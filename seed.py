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

    for i in range(10):
    # for i in range(len(movie_list)):
        title = movie_list[i][8]

        if title <> save_movie:
            print
            print 'new movie:', title
            save_movie = title 
            movie_line = movie_list[i]
            
            director_id_set = get_director_id(movie_line)
            movie_id_set = add_new_movie(movie_line, director_id_set)

# Get actor id's and load movie_actors table
            actor_id_list = get_actor_ids(movie_line)
# TODO Load movie_actors table
# TODO Load movie locations
            # load_movie_actors(actor_id_list, movie_id)
            # print 'writers:', movie_list[i][15]
            # print 'actor_1:', movie_list[i][16]
            # print 'actor_2:', movie_list[i][17]
            # print 'actor_3:', movie_list[i][18]
            # print 'location:', movie_list[i][10]
            # print 'fun_fact:', movie_list[i][11]

            # print 'title:', movie_list[i][8]
            # print 'release year:', movie_list[i][9]
            # print 'location:', movie_list[i][10]
            # print 'fun_fact:', movie_list[i][11]
            # print 'production_company:', movie_list[i][12]
            # print 'distributor:', movie_list[i][13]
            # print 'director:', movie_list[i][14]
            # print 'writers:', movie_list[i][15]
            # print 'actor_1:', movie_list[i][16]
            # print 'actor_2:', movie_list[i][17]
            # print 'actor_3:', movie_list[i][18]
            # print
def get_director_id(movie_line):
    """Process director name to get director id: 
        If director name not in director table, add to director table
        Return director id
    """

    seed_director_name = movie_line[14]
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

    if movie_line[15] == 'N/A':
        movie_writers = None
    else:
        movie_writers = movie_line[15]
       
    new_movie = Movie(
        movie_title = movie_line[8],
        release_year = int(movie_line[9]),    
        production_company = movie_line[12],
        director_id = director_id_set,
        movie_writers = movie_writers,
        movie_distributor = movie_line[13]
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

    # seed_actor_name1 = movie_line[16]
    # seed_actor_name2 = movie_line[17]
    # seed_actor_name3 = movie_line[18]

    # print 'seed_actor_names_input', seed_actor_name1, seed_actor_name2, seed_actor_name3

    for x in range(16, 19):
        if movie_line[x] is not None:
            seed_actor_names.append(movie_line[x])
    # print 'seed_actor_names list: ', seed_actor_names

    
    # For each actor in list, does actor exist in Actor table?
    for x in range(len(seed_actor_names)):

        # print 'line 120 value of x:', x
        try:
            actor_object = Actor.query.filter_by(actor_name=seed_actor_names[x]).one()
            return_actor_id = actor_object.actor_id 
        
        except NoResultFound:
            new_actor = Actor(
            actor_name=seed_actor_names[x]
            )
            db.session.add(new_actor)
            db.session.commit()
# TODO: Use flush session to get actor id's
            # Retrieve actor added above to get actor id 
            actor_object = Actor.query.filter_by(actor_name=seed_actor_names[x]).one()
            return_actor_ids.append(actor_object.actor_id)
          
    print 'return_actor_ids: ', return_actor_ids
    return return_actor_ids

if __name__ == "__main__":
    connect_to_db(app)

    load_movies()