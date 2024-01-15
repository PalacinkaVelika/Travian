from flask import Flask, render_template, request, session, flash, redirect, url_for, get_flashed_messages
import pymongo
import bcrypt
import time
import signal
import json
from DB import DB
from Accounts import Accounts
from CityManager import CityManager
from BuildingManager import BuildingManager
from GameLogicData import GameLogicData

app = Flask(__name__, template_folder='templates')
app.config['SESSION_PERMANENT'] = False
app.secret_key = '745821ba1c21a450ec16b1c325876248eef69a10'

db = DB()
accounts = Accounts()
accounts.load_collection(db)
city_man = CityManager()
city_man.load_collection(db)
building_man = BuildingManager(city_man)
building_man.load_collection(db)


# Session vars
# session['logged_in_id']  # Kdo a jestli je logged in
# session['current_city']  # Vybrané vlastní město na kterém chci pracovat
# session['player_cities']  # Všechna hráčova města



@app.route("/")
@app.route("/home")
@app.route("/main")
def main():
    lgchk = login_check()
    if lgchk != None:
        return lgchk
    
    
    return render_template(
        "main.html", 
        player_id = session['logged_in_id'],
        player_cities = session['player_cities'],
        current_city = session['current_city']
        )

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        session['logged_in_id'] = str(accounts.find_user_id(name, password))
        if session['logged_in_id'] != "None":
            # Předtím než tě hodím na main site tak nastavím session vars pro přihlášeného uživatele
            session['player_cities'] = city_man.player_cities(session['logged_in_id'])
            session['current_city'] = session['player_cities'][0]
            return redirect(url_for("main"))
        flash("Špatný údaje!")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        if accounts.register_new_user(name, password):
            # Create new City and give it to the new account
            new_city_id = city_man.create_random_city(accounts.find_user_id(name, password))
            building_man.create_building_record(new_city_id)
            #Move him to Login
            flash('User registered successfully!')
            return redirect(url_for('login'))
        else:
            flash('Error while saving to the database.')
    return render_template("register.html")

@app.route("/cities")
def cities():
    lgchk = login_check()
    if lgchk != None:
        return lgchk

    return render_template("cities.html")





# Functions i call from buttons and such
@app.route("/logout")
def logout():
    session.clear()
    session.modified = True
    return redirect(url_for('login'))

@app.route("/upgrade_building")
def upgrade_building():
    building_type = request.args.get('building_type')
    if(building_type=="coal" or building_type=="ore" or building_type=="energy"):
        current_building_level = session['current_city']["mine_levels"][building_type]
    elif(building_type=="academy" or building_type=="machinery" or building_type=="specialists"):
        current_building_level = session['current_city']["barracks_levels"][building_type]
        
    wait_time = GameLogicData().building_levels[building_type][str(current_building_level+1)]["wait_time"]
    building_man.start_upgrade_building(session['current_city']["_id"], building_type, wait_time)
    return redirect(url_for('main'))


# Function called from any page without refresh
@app.route('/func')
def func():
    pass
    return ("nothing")

def login_check():
    if 'logged_in_id' not in session or session['logged_in_id'] is None:
        return redirect(url_for("login"))
    return None




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    

