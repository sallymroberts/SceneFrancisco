"""Utility file to update tables after running seed.py to load seed data in json
   format from the San Francisco Film Commission into the data model defined
   in model.py. 
   Function names beginning with "fix_" are used to clean up data. 
   Other functions access API's to update the data model with additional 
   information about the movies and movie locations.
   These functions were run manually, one at at time, throughout the course 
   of the project, and are not yet set up to run automatically in an
   appropriate sequence after re-loading updated San Francisco Film Commission 
   data to the data model. The San Francisco Film Commission publishes
   updated movie data annually. 
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

    count = 0
    loc_obj = Movie_location.query.all()
        
    for obj in loc_obj:

        if not obj.latitude or not obj.longitude:
            location_SF = obj.location_description +', San Francisco, CA'
            g = geocoder.google(location_SF)

# If g.latng not returned, this likely means that the API has rejected
# the request due to exceeding number or frequency of requests. 
            if not g.latlng: 
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
    """Retrieve and print latitude and longitude for one location.
       Use for debugging if error encountered in get_latlng() function 
    """
    
    location_SF = location_description + ', San Francisco, CA'
            
    g = geocoder.google(location_SF)

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
        pass

def fix_movie_titles():
    """Update the movie table from a dictionary of original titles and correct titles: 
    """
    
    correct_title_dict = {
        "D.O.A":"D.O.A.",
        "Doctor Doolittle":"Doctor Dolittle",
        "Dr. Doolittle 2":"Dr. Dolittle 2",
        "Forty Days and Forty Nights":"40 Days and 40 Nights",
        "God is a Communist?* (show me heart universe)":"God is a Communist!?* (show me heart universe)",
        "Mother":"Mother (II)",
        "Panther":"Panther (I)",
        "Swing":"Swing (I)",
        "Terminator - Genisys":"Terminator Genisys",
        "Bridge, The":"Bridge (I), The",
        "Competiton, The":"Competition, The",
        "Fog of War, The":"Fog of War: Eleven Lessons, The",
        "Twisted":"Twisted (I)"
    }
    
    for title in correct_title_dict:
        fix_title(title, correct_title_dict[title])

def fix_title(bad_title, correct_title):
    """Update the movie table with correct movie_title: 
    """  
    try: 
        movie_obj = Movie.query.filter_by(movie_title=bad_title).one()    
        movie_obj.movie_title = correct_title
        db.session.commit()
    except NoResultFound:
        pass

def fix_release_years():
    """Update the movie table from a dictionary of original titles and correct release years: 
    """
    
    correct_release_year_dict = {
        "Ant-Man":2015,
        "Big Sur":2013,
        "Dim Sum: A Little Bit of Heart":1985,
        "Dream for an Insomniac":1996,
        "God is a Communist!?* (Show me heart universe)":2013,
        "Heart and Souls":1993,
        "Hemingway & Gellhorn":2012,
        "Hereafter":2010,
        "I's":2013,
        "Love & Taxes":2015,
        "On the Road":2012,
        "Quitters":2015,
        "San Andreas":2015,
        "Sense8":2015,
        "Terminator Genisys":2015,
        "Ten Commandments, The":1956
    }
    
    for title in correct_release_year_dict:
        fix_release_year(title, correct_release_year_dict[title])

def fix_release_year(movie_title, correct_release_year):
    """Update the movie table with correct release year: 
    """  

    try: 
        movie_obj = Movie.query.filter_by(movie_title=movie_title).one()    
        movie_obj.release_year = correct_release_year
        db.session.commit()
    except NoResultFound:
        pass

def get_movie_info():
    """Update the movies table with plot, genre, movie poster image url: 
    """

    count = 0
    mov_obj = Movie.query.all()
        
    for obj in mov_obj:

        if obj.imdb_id and (not obj.genre or not obj.plot or not obj.image_url):

            movie_info = info_from_imdb_id(obj.imdb_id)
            if movie_info:
                obj.plot = movie_info[0]
                obj.genre = movie_info[1]
                obj.image_url = movie_info[2]                
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

    >>> info_from_imdb_id('tt0377029')
    Plot:  N/A
    [None, u'Documentary', u'http://ia.media-imdb.com/images/M/MV5BMTI0Mzc4OTQwOV5BMl5BanBnXkFtZTcwNDY0NjIzMQ@@._V1_SX300.jpg']
    
    >>> info_from_imdb_id('tt2698124')
    Poster image url:  N/A
    [u'A new religion is born. The CIA investigates.', u'Comedy', None]
    
    >>> info_from_imdb_id('tt1126590')
    [u'A drama about the awakening of the painter Margaret Keane, her phenomenal success in the 1950s, and the subsequent legal difficulties she had with her husband, who claimed credit for her works in the 1960s.', u'Biography, Crime, Drama', u'http://ia.media-imdb.com/images/M/MV5BMjA2ODM5MDE3N15BMl5BanBnXkFtZTgwOTIxNjc1MzE@._V1_SX300.jpg']
    
    >>> info_from_imdb_id('tt00')
    []

    """

    pattern = 'http://www.omdbapi.com/?apikey=[REPLACE]&i={imdb_id}&plot=short&r=json'
    url = pattern.format(imdb_id=urllib.quote(imdb_id))
    r = requests.get(url)
    results_dict = r.json()

    if 'Error' in results_dict:
        return []
    else:
        response = results_dict['Response']

        if results_dict['Plot'] != 'N/A':             
            plot = results_dict['Plot']
        else:
            plot = None
        
        if results_dict['Poster'] != 'N/A': 
            poster_img_url = results_dict['Poster']
        else:
            poster_img_url = None

        genre = results_dict['Genre'] 
 
        return [plot, genre, poster_img_url]

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
                with open(filepath, 'wb') as f:
                    response.raw.decode_content = True
                    shutil.copyfileobj(response.raw, f) 

def fix_title_the():
    """Update the movie table for titles beginning with 'The ' or 'A '
    to format the title for use in alphabetizing the movie list. 
    Original format: 
    "The Bachelor", "A Jitney Elopement"
    Updated format:
    "Bachelor, The", "Jitney Elopement, A"
    """  

    movies = Movie.query.all()
    
    for mov in movies:
        if mov.movie_title[0:4] == 'The ': 
            mov.movie_title = mov.movie_title[4:] + ", The" 
            db.session.commit() 

        elif mov.movie_title[0:2] == 'A ': 
            mov.movie_title = mov.movie_title[2:] + ", A"
            db.session.commit()      

if __name__ == "__main__":
    connect_to_db(app)