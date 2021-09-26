from . import db
from flask_login import UserMixin
from sqlalchemy import func



class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    favs = db.relationship("Favourite")
    comments = db.relationship("Comment")


class Favourite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(300))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    name = db.Column(db.Integer)

#SELECT comment, date FROM Comment where movie_id == 15;
#Comment.query.filter_by(movie_id=15)