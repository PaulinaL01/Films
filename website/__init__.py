from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from website.moviesapi import MoviesAPI
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
DB_NAME = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" #sciekza do bazy
db = SQLAlchemy()
db.init_app(app)
movies = MoviesAPI()


loginManager = LoginManager() #zeby umozliwic logowanie wielu uzytkownikow potrzebujemy loginmanagera
loginManager.login_view = "login" #wskazujemy gdzie ma przekierowac uzytkownika niezalogowanego (musi byc podana nazwa funkcji)
loginManager.init_app(app)

from .models import User, Comment, Favourite, UserMixin
migration = Migrate(app=app, db=db)

from .views import *


@loginManager.user_loader
def load_user(id):
    from .models import User
    return User.query.get(int(id))




