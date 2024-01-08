from flask import Flask, render_template, request, session, flash, redirect, url_for, get_flashed_messages
import pymongo
import bcrypt
import time
from DB import DB
from Accounts import Accounts

app = Flask(__name__, template_folder='templates')
app.secret_key = '745821ba1c21a450ec16b1c325876248eef69a10'

# DB STUFF

#mongo_client = pymongo.MongoClient("mongodb://localhost:27017", connect=True)
#db = mongo_client['traviant'] # Databáze
#account_collections = db['accounts']  # Table
#account_collections.insert_one(register_data)# Upload data
db = DB()
accounts = Accounts()
accounts.load_collection(db)

@app.route("/")
@app.route("/home")
@app.route("/main")
def main():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for("login"))
    return render_template("main.html", logged_in = session['logged_in'])

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        name = request.form.get("username")
        password = request.form.get("password")
  #      user = account_collections.find_one({"login": name})
   #     if user:
    #        if bcrypt.checkpw(password.encode("utf-8"), user["heslo"]):
     #          session['logged_in'] = True
      #          return redirect(url_for("main"))
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
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        register_data = {
                "login" : name,
                "heslo" : hashed_password
        }
        '''
        insert_result = account_collections.insert_one(register_data)
        if insert_result.inserted_id:
            #success
            flash('User registered successfully!')
            return redirect(url_for('login'))
        else:
            #fail
            flash('Error while saving to the database')
        '''
    return render_template("register.html")

@app.route("/budovy")
def budovy():
    if 'logged_in' not in session or session['logged_in'] is None:
        return redirect(url_for("login")) 
    
    return render_template("budovy.html")



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

    

