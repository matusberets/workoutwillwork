import os
import sys
import psycopg2
import psycopg2.extras

#from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, error, connect_db, g, get_db, debug_print


# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloadedvs
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#global variable list for storing chosen picture
chosen_exercise = []

# default page
@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "GET":
        return render_template("register.html")
    else:
        name = request.form.get("username")
        if not name:
            return error("You must provide a name")
        password = request.form.get("password")
        confirm = request.form.get("confirmation")
        if not password:
            return error("You must provide password")
        if not confirm:
            return error("You must confirm your password")
        if password != confirm:
            return error("Your passwords do not match, confirm identical password")
        else:
            db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
            db.execute("INSERT INTO users (username, hash) VALUES (%s,%s)", (name, generate_password_hash(password)))

            # Postgresql to commit query
            get_db().commit()
            
    return redirect("/")


# Login function used from CS50 ProblemSet no.8. Thank you for that CS50 team !
@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()
    if request.method == "POST":
        if not request.form.get("username"):
            return error("You must provide username !")
        elif not request.form.get("password"):
            return error("You must provide password !")
        
        username = request.form.get("username")

        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
        db.execute("SELECT * FROM users WHERE username = (%s)", (username,))
        rows = db.fetchall()
        
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return error("Invalid username or password !")

        session["user_id"] = rows[0]["id"]

        # store user name into session to be displayed after login
        session["user_name"] = rows[0]["username"]

        return redirect("/pickup")

    else:
        return render_template("login.html")


# choose an exercise
@app.route("/pickup", methods=["GET", "POST"])
def pickup():
    if request.method == "GET":

        #debug
        debug_print()
        
        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
        db.execute("SELECT exercise_name FROM exercise_list")
        rows = db.fetchall()

        return render_template("/pickup.html", rows=rows)

    else:
        #debug
        debug_print()
        
        # take chosen exercise, save into variable and then load query from db where chosen ex. name and picture name matches, so the picture can be rendered in html
        exlistname = request.form.get("exercise_list")
        # save chosen exercise into session, to be later used for database insertion line 144
        session["chosen_exercise"] = request.form.get("exercise_list")
        
        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
        db.execute("SELECT picture_name FROM exercise_list WHERE exercise_name = (%s)", (exlistname,))
        data = db.fetchall()

        session["picture_name"] = data[0]["picture_name"]

        return render_template("/exercise.html", chosen_exercise=session["picture_name"], exercise_name=session["chosen_exercise"])


# Choosing from various type of exercises show chosen exercise header and a picture,
# let user define amount of weight lifted, define number of repetitions and possible text comments
@app.route("/exercise", methods=["GET", "POST"])

@login_required
def exercise():
    if request.method == "GET":

        #debug
        debug_print()

        return render_template("exercise.html")
    else:

        #debug
        debug_print()

        # assign user input into variables, so these can be written into database
        # serie no.1
        series1 = request.form.get("series1")
        reps1 = request.form.get("reps1")
        weight1 = request.form.get("weight1")
        if not reps1:
            return error("You must provide reps amount !")
        if not weight1:
            return error("You must provide weight amount !")
        # serie no.2
        series2 = request.form.get("series2")
        reps2 = request.form.get("reps2")
        weight2 = request.form.get("weight2")
        if not reps2:
            return error("You must provide reps amount !")
        if not weight2:
            return error("You must provide weight amount !")
        # serie no.3
        series3 = request.form.get("series3")
        reps3 = request.form.get("reps3")
        weight3 = request.form.get("weight3")
        if not reps3:
            return error("You must provide reps amount !")
        if not weight3:
            return error("You must provide weight amount !")
        # serie no.4
        series4 = request.form.get("series4")
        reps4 = request.form.get("reps4")
        weight4 = request.form.get("weight4")
        if not reps4:
            return error("You must provide reps amount !")
        if not weight4:
            return error("You must provide weight amount !")

        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)        
        db.execute("INSERT INTO history (id, exercise_name, series, reps, weight) VALUES (%s,%s,%s,%s,%s)", (session["user_id"], session["chosen_exercise"], series1, reps1, weight1))    
        get_db().commit()

        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)        
        db.execute("INSERT INTO history (id, exercise_name, series, reps, weight) VALUES (%s,%s,%s,%s,%s)", (session["user_id"], session["chosen_exercise"], series2, reps2, weight2))
        get_db().commit()

        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)        
        db.execute("INSERT INTO history (id, exercise_name, series, reps, weight) VALUES (%s,%s,%s,%s,%s)", (session["user_id"], session["chosen_exercise"], series3, reps3, weight3))
        get_db().commit()

        db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)        
        db.execute("INSERT INTO history (id, exercise_name, series, reps, weight) VALUES (%s,%s,%s,%s,%s)", (session["user_id"], session["chosen_exercise"], series4, reps4, weight4)) 
        get_db().commit()
        
        #debug
        debug_print()

        return redirect("/pickup")


# show user's history, what exercise, amount of weights, number of repetitions was done by a user
@app.route("/history")
@login_required
def history():

    #debug
    debug_print()

    db = get_db().cursor(cursor_factory=psycopg2.extras.DictCursor)
    #select data to be shown based on user logged in
    db.execute("SELECT datetime, exercise_name, series, reps, weight FROM history WHERE id = (%s)", (session["user_id"],))
    rows = db.fetchall() 

    #debug
    debug_print()

    return render_template("history.html", rows=rows)


@app.route("/logout")
def logout():
    session.clear()     
    return redirect("/")


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'psql'):
        g.psql.close()
        print("Connection closed !")