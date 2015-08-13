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

    # if session["user_id"]:
    #     pass
    # else:
    #     session["user_id"] = None
    return render_template("homepage.html")

@app.route('/movies')
def movie_list():
    """Show list of movies."""

    movies = Movie.query.order_by(Movie.movie_title).all()

    return render_template("movie_list.html", movies=movies)

@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    """Show movie detail."""

    movie = Movie.query.filter_by(movie_id=movie_id).one()
    locations = Movie_location.query.filter_by(movie_id=movie_id).all()
    # actors = Movie_actor.query.filter_by(movie_id=movie_id).all()
    # print "Actor: ", actors
    # director_obj = Director.query.filter_by(movie.director_id=director.director_id).all()
    # print "Director: ", director_obj

    return render_template("movie_detail.html", movie=movie, locations=locations)
##############################################################################
# Helper functions

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()

