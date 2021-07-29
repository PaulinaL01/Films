from . import db
from flask_login import UserMixin



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    favs = db.relationship("Favourite")

class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))