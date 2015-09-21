"""Models and database functions for Scene Francisco project."""


from flask_sqlalchemy import SQLAlchemy

# This is the connection to the SQLite database available through the
# Flask-SQLAlchemy helper library. On this, find the `session` object,
# to do most interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Define tables

class Director(db.Model):

    __tablename__ = "directors" 

    director_id = db.Column(db.Integer, primary_key=True)
    director_name = db.Column(db.String(50), nullable=False) 

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


    director_rel = db.relationship(
        'Director',
        backref=db.backref('movies', order_by=movie_id))

    actors = db.relationship(
        'Actor',
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

    movie_location_rel = db.relationship(
        'Movie',
        backref=db.backref(
            'locations', order_by=location_id))

class Movie_actor(db.Model):

    __tablename__ = "movie_actors" 

    movie_actor_id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    actor_id = db.Column(db.Integer, db.ForeignKey('actors.actor_id'), nullable=False)

    movie_actor_rel = db.relationship(
        'Movie',
        backref=db.backref(
            'movie_actors', order_by=actor_id))

    actor_rel = db.relationship(
        'Actor',
        backref=db.backref(
            'movie_actors', order_by=movie_id))

class Actor(db.Model):

    __tablename__ = "actors" 

    actor_id = db.Column(db.Integer, primary_key=True)
    actor_name = db.Column(db.String(50), nullable=False) 

##############################################################################
# Functions

def connect_to_db(app):
    """Connect the database to the Flask app."""

    # Configure to use SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sf_movies.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # For convenience, run module interactively to work directly with the database

    from server import app
    connect_to_db(app)
    print "Connected to DB."