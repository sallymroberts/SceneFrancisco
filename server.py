""" Scene Francisco server """

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import Movie, Movie_location, Movie_actor, Actor, Director, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound

import requests, time


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/movies')
def movie_list():
    """Show list of movies. 
    If user selected genre: subset by genre.
    Else: If user entered title search, subset by partial/full title
    Else: display entire movie list.
    """
    
    user_genre = None
    title_search = None

    if 'genre' in request.args:
        user_genre = request.args['genre']
        if user_genre == 'All':
            movies = Movie.query.order_by(Movie.movie_title).all()
        else:
            movies = Movie.query.filter(Movie.genre.like("%" + user_genre + "%")).all()

    elif 'title_search' in request.args:
        title_search = request.args['title_search']
        if title_search[0:4] == "The ":
            title_search = title_search[4:]
        elif title_search[0:2] == "A ":
            title_search = title_search[2:]
        movies = Movie.query.filter(Movie.movie_title.ilike("%" + title_search + "%")).all()
  
    else: 
        movies = Movie.query.order_by(Movie.movie_title).all()

    return render_template("movie_list.html", movies=movies, genre=user_genre)

@app.route('/movies/<int:movie_id>')
def movie_detail(movie_id):
    """Show movie detail."""

    movie = Movie.query.filter_by(movie_id=movie_id).one()
    locations = Movie_location.query.filter_by(movie_id=movie_id).all()

    json_compiled = {}
    sf_location_list = [] 

    for location in locations:
        dict_key = str(location.latitude) + str(location.longitude)
        
        if location.latitude == 37.7749295 and location.longitude == -122.4194155:
            sf_location_list.append(location.location_description)

        elif dict_key in json_compiled:
            json_compiled[dict_key]['desc'] += "; " + location.location_description 

        else:

            json_compiled[dict_key] = {}
            json_compiled[dict_key]['lat'] = location.latitude
            json_compiled[dict_key]['lng'] = location.longitude
            json_compiled[dict_key]['desc'] = location.location_description

    return render_template("movie_detail.html", movie=movie, film_locations=json_compiled, sf_location_list=sf_location_list)
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

