""" Scene Francisco server """

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Movie, Movie_location, Movie_actor, Actor, Director, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    if session["user_id"]:
        pass
    else:
        session["user_id"] = None
    return render_template("homepage.html")

##############################################################################
# Helper functions

