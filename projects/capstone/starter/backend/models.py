import os
import datetime
import json
from sqlalchemy import Column, String, Integer, DateTime
from flask_sqlalchemy import SQLAlchemy
#from dotenv import load_dotenv

#load_dotenv()

#database_name = "castingagency"
#base_path = os.environ["DATABASE_PATH"]
#database_path='{}/{}'.format(base_path, database_name)
#db = SQLAlchemy()

'''
setup_db(app) -   binds a flask application and a SQLAlchemy services
'''
# connect to heroku db
database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

class Actor(db.Model):
    '''model to be created for actors'''
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)

    '''
        insert /update / delete  for the model actors along with the format to be return while read operations
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

class Movie (db.Model):
    '''model to be created for movies'''
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), unique=True, nullable=False)
    release_date = Column(DateTime(), nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
    
    '''
        insert /update / delete  for the model movies along with the format to be return while read operation
            movie = Movie(title=movie_title, release_date=release_date)
    '''
    
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }