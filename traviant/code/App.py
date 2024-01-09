from flask import Flask, render_template, request, session, flash, redirect, url_for, get_flashed_messages
import pymongo
import bcrypt
import time
from DB import DB
from Accounts import Accounts
from City import City

app = Flask(__name__, template_folder='templates')
app.secret_key = '745821ba1c21a450ec16b1c325876248eef69a10'

db = DB()
accounts = Accounts()
accounts.load_collection(db)
city = City()
city.load_collection(db)

# vrací Cursor a ne Dictionary
city_list = list(city.region_cities(0))

@app.route("/")
@app.route("/home")
@app.route("/main")
def main():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for("login"))
    city.create_new_city(0,0)
    return render_template("main.html", logged_in = session['logged_in'])

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        if accounts.login_user(name, password):
            session['logged_in'] = True
            return redirect(url_for("main"))
        flash("Takový uživatel neexistuje")
    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
        if accounts.register_new_user(name, password):
            flash('User registered successfully!')
            return redirect(url_for('login'))
        else:
            flash('Error while saving to the database.')
    return render_template("register.html")

@app.route("/cities")
def cities():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for("login")) 
    

    return render_template("cities.html", city_list = city_list)





# Functions i call from buttons and such
@app.route("/logout")
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))


# Function called from any page without refresh
@app.route('/func')
def func():
    pass
    return ("nothing")






if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    

