import requests
from flask import Flask, render_template, request, url_for, redirect, flash
from flask_login import login_required, login_user, logout_user, current_user
from . import app, db, User, movies
from werkzeug.security import generate_password_hash
from .forms import LoginForm, SignUpForm
from .models import Favourite


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
@app.route("/overview/<int:id>", methods=["GET", "POST"])
def overview(id):
    id = str(id)
    link_overview = 'https://api.themoviedb.org/3/movie/'+ id + "?api_key=d086e02925aea6ae99f8b04207381382"
    link_overview = requests.get(link_overview).json()
    pos='https://image.tmdb.org/t/p/w400'+link_overview['poster_path']

    if request.method == "POST":

        favourite = Favourite(name=id, user_id=current_user.id)
        db.session.add(favourite)
        db.session.commit()
        print('added to favourite')
        flash("Dzieki za glos", category="success")

    return render_template("overview.html",actor=actor, movies=movies.getPopular(), link_overview=link_overview, pos=pos, favs = current_user.favs, cast=movies.getCast(id))


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
        login_user(user, remember=True)
        flash("Zalogowano!", category="success")
        return redirect(url_for("home"))
    else:
        for error in form.login.errors:
            flash(error, category="warning")
        for error in form.password.errors:
            flash(error, category="warning")

    return render_template("login.html", current_user=current_user, form=form)


@login_required
@app.route("/favourite", methods=["GET", "POST"])
def favourite():

    favs = current_user.favs
    fav_length = len(favs)
    fav_list = []#title
    fav_posters = []
    fav_ids = []

    for c in favs:
        fav = 'https://api.themoviedb.org/3/movie/' + str(c.name) + "?api_key=d086e02925aea6ae99f8b04207381382"
        all_fav = requests.get(fav).json()
        fav_id = str(c.name)
        fav_title = all_fav['original_title']
        fav_poster = 'https://image.tmdb.org/t/p/w400' + all_fav['poster_path']
        fav_list.append(fav_title)
        fav_posters.append(fav_poster)
        fav_ids.append(fav_id)



    return render_template("favourite.html", favs = favs,  fav_list=fav_list, fav_posters=fav_posters,fav_length=fav_length,fav_ids=fav_ids)

@login_required
@app.route("/delete/<name>")
def delete_complaint(name):
    f = Favourite.query.filter_by(name=name)
    if f:
        f.delete()
        db.session.commit()
        print("favourite movie deleted")
    return redirect(url_for("favourite"))

@login_required
@app.route("/actor/<int:actor_id>", methods=["GET", "POST"])
def actor(actor_id):
    link_actor = 'https://api.themoviedb.org/3/person/'+str(actor_id)+'?api_key=d086e02925aea6ae99f8b04207381382&language=en-US'
    link_actor = requests.get(link_actor).json()
    biography_actor = link_actor['biography']
    birthday_actor = link_actor['birthday']
    deathday_actor = link_actor['deathday']
    name_actor = link_actor['name']
    place_of_birth_actor = link_actor['place_of_birth']
    profile_path_actor ='https://image.tmdb.org/t/p/w400'+ str(link_actor['profile_path'])


    return render_template('actor.html', link_actor=link_actor,biography_actor=biography_actor,birthday_actor=birthday_actor, deathday_actor=deathday_actor, name_actor=name_actor, place_of_birth_actor=place_of_birth_actor,profile_path_actor=profile_path_actor)