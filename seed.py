"""Utility file to seed San Francisco film locations database from public
    SF data set in JSON format
"""

from model import Director, Movie, Movie_location, Movie_actor, Actor, connect_to_db, db
from server import app
from sqlalchemy.orm.exc import NoResultFound
import json

def load_movies():
    """Load movies from Film_Locations_in_San_Francisco.csv into database."""
    
# Open seed data file and create movie list from json dictionary
    seed_movies_file = open("movie_seed.json")
    file_text = seed_movies_file.read()
    json_dict = json.loads(file_text)
    movie_list = json_dict['data']

    save_movie = None

    # for i in range(60):
    for i in range(len(movie_list)):
        title = movie_list[i][8].strip()
        movie_line = movie_list[i]
        # import pdb; pdb.set_trace()
        if title <> save_movie:
            print
            print 'new movie:', title
            save_movie = title 
                   
            director_id_set = get_director_id(movie_line)
            movie_id_set = add_new_movie(movie_line, director_id_set)

# Get actor id's and load movie_actors table
            actor_id_list = get_actor_ids(movie_line)
            if actor_id_list != []:
                load_movie_actors(movie_id_set, actor_id_list)
            
# Load movie locations
        if movie_list[i][10] is not None:
            load_movie_location(movie_line, movie_id_set)

def get_director_id(movie_line):
    """Process director name to get director id: 
        If director name not in director table, add to director table
        Return director id
    """

    seed_director_name = movie_line[14].strip()
    return_director_id = None
    
    try:
        director_object = Director.query.filter_by(director_name=seed_director_name).one()
        return_director_id = director_object.director_id 
        
    except NoResultFound:
        new_director = Director(
        director_name=seed_director_name
        )
        db.session.add(new_director)
        db.session.flush()
        return_director_id = new_director.director_id
        db.session.commit()
      
    return return_director_id

def add_new_movie(movie_line, director_id_set):
    """Add new movie to Movie table

    """
    return_movie_id = None

    if movie_line[12] in ('N/A', 'NA') or movie_line[12] is None:
        production_company = None
    else:
        production_company = movie_line[12].strip()

    if movie_line[13] in ('N/A', 'NA') or movie_line[13] is None:
        movie_distributor = None
    else:
        movie_distributor = movie_line[13].strip()

    if movie_line[15] in ('N/A', 'NA') or movie_line[15] is None:
        movie_writers = None
    else:
        movie_writers = movie_line[15].strip()

    new_movie = Movie(
        movie_title = movie_line[8].strip(),
        release_year = int(movie_line[9].strip()),    
        production_company = production_company,
        director_id = director_id_set,
        movie_writers = movie_writers,
        movie_distributor = movie_distributor
        )
    db.session.add(new_movie)
    db.session.flush()
    return_movie_id = new_movie.movie_id
    db.session.commit()
    
    return return_movie_id

def get_actor_ids(movie_line):
    """Process 3 actor name fields to get actor ids: 
    For each actor name that is not null:
        If new, add to Actor table
    Return list of 0 - 3 actor id's
    """

    seed_actor_names = []
    return_actor_ids = []

    for x in range(16, 19):
        if movie_line[x] is not None:
            seed_actor_names.append(movie_line[x].strip())
    
    # For each actor in list, does actor exist in Actor table?
    for x in range(len(seed_actor_names)):
        try:
            actor_object = Actor.query.filter_by(actor_name=seed_actor_names[x]).one() 
            return_actor_ids.append(actor_object.actor_id)
        
        except NoResultFound:
            new_actor = Actor(
            actor_name=seed_actor_names[x]
            )
            db.session.add(new_actor)
            db.session.flush()
            return_actor_ids.append(new_actor.actor_id)
    db.session.commit()
          
    return return_actor_ids

def load_movie_actors(movie_id_set, actor_id_list):
    """Add 1-3 actors for a movie to the movie_actors table: 
    """

    for i in range(len(actor_id_list)):
        
        new_movie_actor = Movie_actor(
        movie_id=movie_id_set,
        actor_id=actor_id_list[i]
        )
        db.session.add(new_movie_actor)
        
    db.session.commit()

def load_movie_location(movie_line, movie_id_set):
    """Add location for a movie to the movie_locations table: 
    """
    if movie_line[11] is None:
        fun_fact = None
    else:
        fun_fact = movie_line[11].strip()
        
    new_movie_location = Movie_location(
    movie_id=movie_id_set,
    location_description=movie_line[10].strip(),
    latitude=None,
    longitude=None,
    fun_fact=fun_fact
    )

    db.session.add(new_movie_location)
        
    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    load_movies()