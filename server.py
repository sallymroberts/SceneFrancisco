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
    user_title_search = None

    if 'genre' in request.args:
        user_genre = request.args['genre']
        movies = get_movies_by_genre(user_genre)

    elif 'title_search' in request.args:
        user_title_search = request.args['title_search']
        movies = get_movies_by_title(user_title_search)
        
    else: 
        movies = Movie.query.order_by(Movie.movie_title).all()

    return render_template("movie_list.html", \
                    movies=movies, \
                    genre=user_genre)

@app.route('/<int:movie_id>')
def movie_detail(movie_id):
    """Show movie detail."""

    movie = Movie.query.filter_by(movie_id=movie_id).one()
    title = format_title(movie.movie_title)
    actors = format_actors(movie.actors)
    location_dict, sf_location_list = get_locations(movie_id)

    return render_template("movie_detail.html",\
                    movie=movie, \
                    film_locations=location_dict, \
                    sf_location_list=sf_location_list, \
                    actors=actors, \
                    title=title)
##############################################################################
# Helper functions

def get_movies_by_genre(user_genre):
    """ Get subset of movies based on genre. 
        Accepts genre entered by user, returns movies.

    """
    if user_genre == 'All':
        movies = Movie.query.order_by(Movie.movie_title).all()
    else:
        movies = Movie.query.filter(Movie.genre.like("%" + user_genre + "%"))\
            .order_by(Movie.movie_title)\
            .all()

    return movies

def get_movies_by_title(user_title_search):
    """ Get subset of movies based on full/partial title search string. 
        Accepts title search string entered by user, returns movies.
        First, remove "the " and "a " from beginning of user title search string 
        because titles beginning with 'The ' and 'A ' are formatted like
        'Bachelor, The' and 'Jitney Elopement, A', to facilitate 
        alphabetizing the movie list.

    """

    if user_title_search[0:4] in ("The ", "the "):    
        user_title_search = user_title_search[4:]
    elif user_title_search[0:2] in ("A ", "a "):
        user_title_search = user_title_search[2:]

    movies = Movie.query.filter(Movie.movie_title.ilike("%" + user_title_search + "%"))\
        .order_by(Movie.movie_title)\
        .all()

    return movies

def format_title(input_title):
    """ Format movie titles from Movies table for display on movie detail page.
        Accepts title, returns formatted title.
        Most titles are already formatted as needed. Titles beginning with 
        'The ' and 'A '  are formatted in the Movies table to facilitate 
        alphabetizing the movie list, in the format: 
        'Bachelor, The'
        'Jitney Elopement, A'
        
        This function reformats these titles in the format: 
        'The Bachelor'
        'A Jitney Elopement'.
    """

    if input_title[-5:] in (", The", ", the"):   
        title = "The " + input_title[:-5]
    elif input_title[-3:] in (", A", ", a"):
        title = "A " + input_title[:-3]
    else: 
        title = input_title

    return title

def format_actors(input_actors):
    """ Format 0-3 actors into comma-separated list for display on 
        movie detail page.
        Accepts list of actors, returns comma-separated string of actors    
    """

    actors = None

    if input_actors:
        actor_list = []
        for actor in input_actors:
            actor_list.append(actor.actor_name)
        s = ", "
        actors = s.join(actor_list)

    return actors

def get_locations(movie_id):
    """ Retrieve filming locations
        Accepts movie id, returns filming locations formatted into 2 structures:

        1. Location dictionary for locations with meaningful latitude & longitude
        2. Location list for locations for which the Google maps API could not
           identify a specific location from the description. For these locations, 
           the Google maps API returns latitude 37.7749295 and longitude -122.419415,
           the generic coordinates for San Francisco.
           Load these locations into a list, to display without markers on the movie
           detail page, because the markers would be misleading.
    """

    locations = Movie_location.query.filter_by(movie_id=movie_id).all()

    location_dict = {}
    sf_location_list = [] 

    for location in locations:
        dict_key = str(location.latitude) + str(location.longitude)

        if location.latitude == 37.7749295 and location.longitude == -122.4194155:
            sf_location_list.append(location.location_description)

        elif dict_key in location_dict: 
            location_dict[dict_key]['desc'] += "; <p>" + location.location_description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = location.latitude
            location_dict[dict_key]['lng'] = location.longitude
            location_dict[dict_key]['desc'] = location.location_description

    return location_dict, sf_location_list

# Setup up variables based on environment (Heroku, local) 
PORT = int(os.environ.get("PORT", 5000))
DEBUG = "NO_DEBUG" not in os.environ

if __name__ == "__main__":
    app.debug = DEBUG
    connect_to_db(app)
    app.run(host="0.0.0.0", port=PORT)    