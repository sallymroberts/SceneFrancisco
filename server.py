""" Scene Francisco server """

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_debugtoolbar import DebugToolbarExtension

from model import Movie, Movie_location, Movie_actor, Actor, Director, connect_to_db, db

from sqlalchemy.orm.exc import NoResultFound

import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_TOKEN']
# app.config['SECRET_KEY'] = os.environ['FLASK_SECRET_KEY']

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def movie_list():
    """Show list of movies on home page. 
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
            movies = Movie.query.filter(Movie.genre.like("%" + user_genre + "%"))\
                .order_by(Movie.movie_title)\
                .all()

    elif 'title_search' in request.args:
        title_search = request.args['title_search']
        
        if title_search[0:4] in ("The ", "the "):    
            title_search = title_search[4:]
        elif title_search[0:2] in ("A ", "a "):
            title_search = title_search[2:]

        movies = Movie.query.filter(Movie.movie_title.ilike("%" + title_search + "%"))\
        .order_by(Movie.movie_title)\
        .all()
  
    else: 
        movies = Movie.query.order_by(Movie.movie_title).all()

    return render_template("movie_list.html", \
                    movies=movies, \
                    genre=user_genre)

@app.route('/<int:movie_id>')
def movie_detail(movie_id):
    """Show movie detail."""

    movie = Movie.query.filter_by(movie_id=movie_id).one()

    print "Original title: ", movie.movie_title 
    
    if movie.movie_title[-5:] in (", The", ", the"):   
        title = "The " + movie.movie_title[:-5]
    elif movie.movie_title[-3:] in (", A", ", a"):
        title = "A " + movie.movie_title[:-3]
    else: 
        title = movie.movie_title

    print "title: ", title
        
    locations = Movie_location.query.filter_by(movie_id=movie_id).all()

    json_compiled = {}
    sf_location_list = [] 

    for location in locations:
        dict_key = str(location.latitude) + str(location.longitude)
        
        if location.latitude == 37.7749295 and location.longitude == -122.4194155:
            sf_location_list.append(location.location_description)

        elif dict_key in json_compiled: 
            json_compiled[dict_key]['desc'] += "; <p>" + location.location_description

        else:

            json_compiled[dict_key] = {}
            json_compiled[dict_key]['lat'] = location.latitude
            json_compiled[dict_key]['lng'] = location.longitude
            json_compiled[dict_key]['desc'] = location.location_description

    return render_template("movie_detail.html",\
                    movie=movie, \
                    film_locations=json_compiled, \
                    sf_location_list=sf_location_list, \
                    title=title)
##############################################################################
# Helper functions

# Setup up variables based on environment (Heroku, local) 
PORT = int(os.environ.get("PORT", 5000))
DEBUG = "NO_DEBUG" not in os.environ

if __name__ == "__main__":
    app.debug = DEBUG
    connect_to_db(app)
    app.run(host="0.0.0.0", port=PORT)    