import random

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

    return render_template("overview.html", actor=actor, movies=movies.getPopular(), link_overview=link_overview, pos=pos, favs = current_user.favs, cast=movies.getCast(id))


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
    favourites = []
    for fav in current_user.favs:
        favourites.append(movies.getMovieDetails(fav.name))

    return render_template("favourite.html", favourites=favourites)


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
    return render_template('actor.html',all_actors = movies.getActor(actor_id) )


@login_required
@app.route("/random", methods=["GET", "POST"])
def random_movie():
    while True:
        movie_random = random.randint(1,29949)
        link_random =requests.get(
        'https://api.themoviedb.org/3/movie/'+str(movie_random)+'?api_key=d086e02925aea6ae99f8b04207381382&language=en-US').json()

        if 'success' in link_random:
            continue

        if 'id' in link_random and link_random['poster_path']!=None:
            return redirect(f"overview/{movie_random}")

        elif 'id' in link_random and link_random['poster_path'] == None:
            random_poster = 'https://pixabay.com/get/g96776ca595ca4bced6d9bc99e584deb15ef40333e744a28c9932fbc52680ebd5a9a219fbd2cd0cece9c4674cea2a2072.svg'
            random_title = link_random["original_title"]
            random_overview = link_random["overview"]
            random_vote = link_random['vote_average']
            random_release = link_random['release_date']
            for a in link_random['genres']:
                random_genres = a['name']

            return render_template('random.html', random_genres=random_genres, random_poster=random_poster, random_title=random_title, random_overview=random_overview, random_vote=random_vote, random_release=random_release, cast=movies.getCast(str(movie_random)), actor=actor)

        # if request.method == "POST":
        #     favourite = Favourite(name=movie_random, user_id=current_user.id)
        #     db.session.add(favourite)
        #     db.session.commit()
        #     print('added to favourite')
        #     flash("Dzieki za glos", category="success")
        #
        #     return render_template('random.html', favs = current_user.favs)



