import requests
from flask import Flask, render_template, request, url_for, redirect, flash
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash
# from . import app, db, User
from werkzeug.security import generate_password_hash
from .forms import LoginForm, SignUpForm,Complaint
from flask_sqlalchemy import SQLAlchemy
import os
from website.movies import Movies

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
DB_NAME = "database.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}" #sciekza do bazy
db = SQLAlchemy()
db.init_app(app)
movies = Movies()

if not os.path.exists(DB_NAME): #jesli plik nie ostnieje
    from .models import User
    db.create_all(app=app)
    print("DB created!")

loginManager = LoginManager() #zeby umozliwic logowanie wielu uzytkownikow potrzebujemy loginmanagera
loginManager.login_view = "login" #wskazujemy gdzie ma przekierowac uzytkownika niezalogowanego (musi byc podana nazwa funkcji)
loginManager.init_app(app)

@loginManager.user_loader
def load_user(id):
    from .models import User
    return User.query.get(int(id))

@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@login_required
@app.route("/")
def home():
    return render_template("home.html", movies=movies.getPopular())

@login_required
@app.route("/overview/<int:id>")
def overview(id):
    id = str(id)
    link_overview = 'https://api.themoviedb.org/3/movie/'+ id + "?api_key=d086e02925aea6ae99f8b04207381382"
    link_overview = requests.get(link_overview).json()

    pos='https://image.tmdb.org/t/p/w400'+link_overview['poster_path']
    credits = 'https://api.themoviedb.org/3/movie/' + id + "/credits?api_key=d086e02925aea6ae99f8b04207381382"
    all_credits = requests.get(credits).json()


    full_cast = all_credits['cast']
    print(full_cast)
    cast_length = len(full_cast)
    name_list = []
    pic_list = []
    role_list = []
    id_list = []

    for i,actor in enumerate(all_credits['cast']):
        actor_name = actor['name']
        actor_pic = 'https://image.tmdb.org/t/p/w400' + str(actor['profile_path'])
        actor_role = actor['character']
        actor_id = actor['id']
        name_list.append(actor_name)
        pic_list.append(actor_pic)
        role_list.append(actor_role)
        id_list.append(actor_id)
    return render_template("overview.html", movies=movies.getPopular(), link_overview=link_overview, pos=pos, all_credits=all_credits, full_cast=full_cast, name_list=name_list, role_list=role_list, pic_list=pic_list, cast_length=cast_length)

@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if User.query.filter_by(login=form.login.data).first():
            flash("Podany uzytkownik juz istnieje", category="warning")
        else:
            flash("Utworzono uzytkownika", category="success")
            user = User(login=form.login.data, email=form.email.data,
                        password=generate_password_hash(form.password1.data))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("login"))
    else:
        for error in form.login.errors:
            flash(error, category="warning")
        for error in form.email.errors:
            flash(error, category="warning")
        for error in form.password1.errors:
            flash(error, category="warning")

    return render_template("sign_up.html", current_user=current_user, form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():  # jesli formularz udalo sie poprawnie wypelnic
        user = User.query.filter_by(login=form.login.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=True)
                flash("Zalogowano!", category="success")
                return redirect(url_for("home"))
            else:
                flash("Niepoprawne haslo!", category="warning")
        else:
            flash("Niepoprawne dane logowania", category="warning")
    else:
        for error in form.login.errors:
            flash(error, category="warning")
        for error in form.password.errors:
            flash(error, category="warning")

    return render_template("login.html", current_user=current_user, form=form)

