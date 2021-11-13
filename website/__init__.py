from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from numpy._distributor_init import basedir
from website.moviesapi import MoviesAPI
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_dance.contrib.github import make_github_blueprint, github
import os
from flask_avatars import Avatars

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
app = Flask(__name__)
avatars = Avatars(app)
app.config['AVATARS_SAVE_PATH'] = os.path.join(basedir, 'avatars')
app.config['SECRET_KEY'] = '1234'
DB_NAME = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" #sciekza do bazy
db = SQLAlchemy()
db.init_app(app)
movies = MoviesAPI()

blueprint = make_github_blueprint(
    client_id="f8c198030ee1ff5d4472",
    client_secret="0909003f1c5c0e1f674d56d626d3e9864eae96db",
)
app.register_blueprint(blueprint, url_prefix="/github_login")

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

with app.app_context():
    if not User.query.filter_by(login="admin").first():
        user = User(login="admin", password=generate_password_hash("A1234567"), admin=True)
        db.session.add(user)
        db.session.commit()



