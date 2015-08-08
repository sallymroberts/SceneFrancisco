"""Utility file to do map functions 
"""

from model import Director, Movie, Movie_location, Movie_actor, Actor, connect_to_db, db
from server import app
from sqlalchemy.orm.exc import NoResultFound
import json
import geocoder
from time import sleep

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
                # print "obj.latitude after: ", obj.latitude
                # print "obj.longitude after: ", obj.longitude
                # print
                
                db.session.add(obj)
                sleep(0.5)


                count += 1
                if count > 200:
                    db.session.commit() 
                    count = 0

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    get_latlng()