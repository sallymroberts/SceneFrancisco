"""Models and database functions for Scene Francisco project."""


from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Part 1: Compose ORM

class Director(db.Model):

    __tablename__ = "directors" 

    director_id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return "<director_id=%d director_name=%s>" % (self.director_id, self.director_name)

class Movie(db.Model):

    __tablename__ = "movies" 

    movie_id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer)
    production_company = db.Column(db.String(50))
    director_id = db.Column(db.Integer, db.ForeignKey('directors.director_id'))
    movie_writers = db.Column(db.String(50))
    movie_distributor = db.Column(db.String(50))
    imdb_id = db.Column(db.String(9))
    imdb_url = db.Column(db.String(60))
    image_url = db.Column(db.String(75))
    genre = db.Column(db.String(20))
    plot = db.Column(db.Text)


    director_rel = db.relationship('Director',
                           backref=db.backref('movies', order_by=movie_id)
                           )

    actors = db.relationship('Actor',
                        secondary='movie_actors',
                        backref='movies')

    def __repr__(self):
        return "<movie_id=%d title=%s>" % (self.movie_id, self.movie_title)

class Movie_location(db.Model):

    __tablename__ = "movie_locations" 

    location_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    location_description = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    fun_fact = db.Column(db.Text) 

    movie_location_rel = db.relationship('Movie',
                           backref=db.backref('movies', order_by=location_id)
                           )

    def __repr__(self):
        return "<location_id=%d movie_id=%s location_description=%s>" % (self.location_id, self.movie_id, self.location_description)


class Movie_actor(db.Model):

    __tablename__ = "movie_actors" 

    movie_actor_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.actor_id'), nullable=False)

    movie_actor_rel = db.relationship('Movie',
                           backref=db.backref('movie_actors', order_by=actor_id)
                           )
    actor_rel = db.relationship('Actor',
                           backref=db.backref('movie_actors', order_by=movie_id)
                           )

    def __repr__(self):
        return "<movie_actor_id=%d movie_id=%d actor_id=%d>" % (self.movie_actor_id, self.movie_id, self.actor_id)

class Actor(db.Model):

    __tablename__ = "actors" 

    actor_id = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.String(50), nullable=False) 

    def __repr__(self):
        return "<actor_id=%d actor_name=%s>" % (self.actor_id, self.actor_name)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sf_movies.db'
    # app.config['SQLALCHEMY_RECORD_QUERIES'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."