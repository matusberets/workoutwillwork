# I have took an inspiration from CS50 ProblemSet no.8. Thank you for that CS50 team !

import os
import psycopg2
import psycopg2.extras

from flask import redirect, session, render_template, g
from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

# error message function
def error(text):
    return render_template("error.html", text=text)

#estabilish PSQL connection
def connect_db():

    DB_HOST = "ec2-52-211-161-21.eu-west-1.compute.amazonaws.com"
    DB_NAME = "d5gpufg0ht2tcv"
    DB_USER = "jorqzsdckjpref"
    DB_PASS = "e757bbed8d7f33357c6c52e446df4b9863300b89ad7cdfbee42682a247e1e4cd"

    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST)
    return conn

# connect to the database
def get_db():
    """Opens a new database connection if there is none yet for the current application context."""
    if not hasattr(g, 'psql'):
        print("Connection restabilished !")
        g.psql = connect_db()
    return g.psql