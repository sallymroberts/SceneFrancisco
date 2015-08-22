"""Utility file to do update tables after seed data loaded 
"""

from model import Director, Movie, Movie_location, Movie_actor, Actor, connect_to_db, db
from server import app
from sqlalchemy.orm.exc import NoResultFound
import json
import geocoder
from time import sleep

import requests
import urllib
import shutil
import os

def load_imdb_id():
    """ load IMDB id and IMDB url in Movies table
    """
    count = 0
    mov_obj = Movie.query.all()
        
    for mov in mov_obj:

        change = None

        if not mov.imdb_id:
            mov.imdb_id = imdb_id_from_title(mov.movie_title) 
            change = 1   
            

        if mov.imdb_id and not mov.imdb_url:
            mov.imdb_url = 'http://www.imdb.com/title/' + mov.imdb_id + '/?ref_=fn_al_tt_1'
            change = 1

        if change:    
            db.session.add(mov)
            sleep(0.5)

            count += 1
            if count > 200:
                db.session.commit() 
                count = 0

    db.session.commit()

def imdb_id_from_title(title):
    """ return IMDB id for search string

        Args::
            title (str): the movie title search string

        Returns: 
            str. IMDB id, e.g., 'tt0095016' 
            None. If no match was found

        NOTE: I got this function from Johannes Bader at: 
        http://www.johannesbader.ch/2013/11/tutorial-download-posters-with-the-movie-database-api-in-python/

    """
    pattern = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q={movie_title}'
    url = pattern.format(movie_title=urllib.quote(title))
    r = requests.get(url)
    res = r.json()
    # sections in descending order or preference
    for section in ['popular','exact','substring']:
        key = 'title_' + section 
        if key in res:
            return res[key][0]['id']

def get_latlng():
    """Update the movie_locations table with latitude and longitude: 
    """
    # g = geocoder.google('555 Market St., San Francisco, CA')

    count = 0
    loc_obj = Movie_location.query.all()
    # import pdb; pdb.set_trace()
        
    for obj in loc_obj:

        if not obj.latitude or not obj.longitude:
            location_SF = obj.location_description +', San Francisco, CA'
            # print "Loc desc, loc id, movie id: ", obj.location_description, obj.location_id, obj.movie_id            
            # print "obj.latitude before: ", obj.latitude
            # print "obj.longitude before: ", obj.longitude
            # print
            # break
            g = geocoder.google(location_SF)
            # print "Loc desc, loc id, movie id: ", obj.location_description, obj.location_id, obj.movie_id
            if not g.latlng: 
                print g
                print "No latitude / longitude retrieved, stop program"
                print "Loc desc, loc id, movie id: ", obj.location_description, obj.location_id, obj.movie_id 
                break
            else:
                obj.latitude = g.latlng[0]
                obj.longitude = g.latlng[1]
                
                db.session.add(obj)
                sleep(0.5)


                count += 1
                if count > 200:
                    db.session.commit() 
                    count = 0

    db.session.commit()
def get_one_latlng(location_description):
    """Retrieve latitude and longitude for one location: 
    """
    # g = geocoder.google('555 Market St., San Francisco, CA')

    
    location_SF = location_description + ', San Francisco, CA'
            
    g = geocoder.google(location_SF)
    # print "Loc desc, loc id, movie id: ", obj.location_description, obj.location_id, obj.movie_id
    if not g.latlng: 
        print g
        print "No latitude / longitude retrieved"
        print "Location description: ", location_description
        print
    else:
        print "Location description: ", location_description
        print 'latitude = ', g.latlng[0]
        print 'longitude = ', g.latlng[1]
        print

def fix_imdb_ids():
    """Update the movie table from a dictionary of titles and correct imdb_ids: 
    """
    
    correct_imdb_dict = {
        "About a Boy":"tt2666270",
        "Babies":"tt1020938",
        "Class Action":"tt0101590",
        "CSI: NY- episode 903":"tt2338762",
        "D.O.A":"tt0042369",
        "Fandom":"tt0417667",
        "Fathers' Day":"tt0119109",
        "Fearless":"tt0106881",
        "Forty Days and Forty Nights":"tt0243736",
        "Groove":"tt0212974",
        "Heart Beat":"tt0080854",
        "I's":"tt3408708",
        "Jack":"tt0116669",
        "Jade":"tt0113451",
        "Just One Night":"tt0201901",
        "Maxie":"tt0089569",
        "Metro":"tt0119664",
        "Mother":"tt0117091",
        "My Reality":"tt3305266",
        "Panther":"tt0114084",
        "Point Blank":"tt0062138",
        "Rollerball":"tt0246894",
        "Serial":"tt0081485",
        "Shattered":"tt0102900",
        "Swing":"tt0358722",
        "The Bridge":"tt0799954",
        "The Californians":"tt0377043",
        "The Candidate":"tt0068334",
        "The Competiton":"tt0080556",
        "The Love Bug":"tt0064603",
        "To the Ends of the Earth":"tt0040887",
        "Twisted":"tt0315297",
        "Yours, Mine and Ours":"tt0063829"
    }
    
    for title in correct_imdb_dict:
        fix_imdb_id(title, correct_imdb_dict[title])

def fix_imdb_id(movie_title, correct_imdb_id):
    """Update the movie table with correct imdb_id: 
    """  
    try: 
        movie_obj = Movie.query.filter_by(movie_title=movie_title).one()    
        movie_obj.imdb_id = correct_imdb_id
        movie_obj.imdb_url = 'http://www.imdb.com/title/' + correct_imdb_id + '/?ref_=fn_al_tt_1'
        db.session.commit()
    except NoResultFound:
        print "Title not found:", movie_title, correct_imdb_id

def get_movie_info():
    """Update the movies table with plot, genre, movie poster image url: 
    """

    count = 0
    mov_obj = Movie.query.all()
    # import pdb; pdb.set_trace()
        
    for obj in mov_obj:

        if obj.imdb_id and (not obj.genre or not obj.plot or not obj.image_url):

            movie_info = info_from_imdb_id(obj.imdb_id)
            if movie_info:
                obj.plot = movie_info[0]
                # print
                # print 'obj.plot', obj.plot

                obj.genre = movie_info[1]
                # print 'obj.genre', obj.genre

                obj.image_url = movie_info[2]
                # print 'obj.image_url', obj.image_url
                
                db.session.add(obj)
                sleep(0.5)
                count += 1
                if count > 50:
                    db.session.commit() 
                    count = 0

    db.session.commit()
def info_from_imdb_id(imdb_id):
    """ return movie info for search string containing IMDB id

        Args::
            title (str): the imdb id search string

        Returns:         
            short plot description
            movie genre
            movie poster image url
    """

    pattern = 'http://www.omdbapi.com/?apikey=[REPLACE]&i={imdb_id}&plot=short&r=json'
    url = pattern.format(imdb_id=urllib.quote(imdb_id))
    r = requests.get(url)
    results_dict = r.json()
    response = results_dict['Response']
    
    if response:
        if results_dict['Plot'] != 'N/A': 
            plot = results_dict['Plot']
        else:
            plot = None
        genre = results_dict['Genre'] 
        poster_img_url = results_dict['Poster'] 
        return [plot, genre, poster_img_url]
    else: 
        return []

def fix_image_url():
    """Update the movie table with null image_url if value is "N/A" 
    """  

    mov_obj = Movie.query.filter_by(image_url="N/A").all() 

    for mov in mov_obj:
        mov.image_url = None  
        db.session.commit()

def create_movie_image_files():
    """Retrieve movie images using imdb url and 
    store in image folder"""           

    movies = Movie.query.all()

    for mov in movies:
        if mov.image_url:
            path = "./static/images/"


            filename = "image%s.jpg" % mov.movie_id
            filepath = os.path.join(path, filename)
            response = requests.get(mov.image_url, stream=True)
            if response.status_code == 200:
                print response.raw
                with open(filepath, 'wb') as f:
                    response.raw.decode_content = True
                    print response.raw
                    shutil.copyfileobj(response.raw, f)      
def fix_title_the():
    """Update the movie table for titles beginning with 'The' 
    """  

    movies = Movie.query.filter_by(movie.movie_title.like("The%").all()

    for mov in movies:
        mov.movie_title = mov.movie_title[4:] + ", The"
        print mov.movie_title
        # db.session.commit()        

if __name__ == "__main__":
    connect_to_db(app)

    fix_title_the()
    # create_movie_image_files()
    # fix_image_url()
    # get_movie_info()

    # print info_from_imdb_id("tt1855110")
    # print "imdb id invalid: ", info_from_imdb_id("invalid")
    # fix_imdb_id("180", "tt1855110")
    # fix_imdb_ids()

    # get_one_latlng("Powell from Bush and Sutter")
    # get_one_latlng("Crissy Field")
    # get_one_latlng("Broderick from Fulton to McAlister")
    # get_one_latlng("")
    # imdb_id = imdb_id_from_title("Final Destination")
    # print imdb_id
    # get_latlng()
    # load_imdb_id()
