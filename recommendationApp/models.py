from flask_login import UserMixin
from startup import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Artist(db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    name = db.Column(db.String(1000))

class Likes(db.Model):
    pm = db.Column(db.Integer, primary_key=True)
    song_id = db.Column(db.Integer) # primary keys are required by SQLAlchemy
    artist = db.Column(db.String(100))
    user_email = db.Column(db.String(100))
