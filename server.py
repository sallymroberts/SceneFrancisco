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
        
# Remove "the " and "a " from beginning of user title search string 
# because titles beginning with "The " and "A " are formatted like
# "Bachelor, The" and "Jitney Elopement, A", to alphabetize the list 
    
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
    
# Reformat movie titles for display on movie detail page in format:
# "The Bachelor" and "A Jitney Elopement".
# Titles beginning with "The " and "A " are  are formatted like
# "Bachelor, The" and "Jitney Elopement, A", in the Movies table
# in order to alphabetize the movie list correctly

    if movie.movie_title[-5:] in (", The", ", the"):   
        title = "The " + movie.movie_title[:-5]
    elif movie.movie_title[-3:] in (", A", ", a"):
        title = "A " + movie.movie_title[:-3]
    else: 
        title = movie.movie_title
        
    locations = Movie_location.query.filter_by(movie_id=movie_id).all()

    location_dict = {}
    sf_location_list = [] 

    for location in locations:
        dict_key = str(location.latitude) + str(location.longitude)

# The Google maps API returns Latitude 37.7749295 and Longitude -122.419415,
# the generic coordinates for San Francisco, for locations it cannot 
# identify more specifically.
# Pass these locations as a list, to display without markers on the movie detail
# page, because the markers would be misleading

        if location.latitude == 37.7749295 and location.longitude == -122.4194155:
            sf_location_list.append(location.location_description)

        elif dict_key in location_dict: 
            location_dict[dict_key]['desc'] += "; <p>" + location.location_description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = location.latitude
            location_dict[dict_key]['lng'] = location.longitude
            location_dict[dict_key]['desc'] = location.location_description

    return render_template("movie_detail.html",\
                    movie=movie, \
                    film_locations=location_dict, \
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