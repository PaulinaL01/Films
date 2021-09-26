import random
from functools import wraps
from .dekoratory import liked_movie_required, not_log_in

import requests
from flask import Flask, render_template, request, url_for, redirect, flash, session
from flask_login import login_required, login_user, logout_user, current_user
from . import app, db, User, movies
from werkzeug.security import generate_password_hash
from .forms import LoginForm, SignUpForm, CommentForm, Filter_Films
from .models import Favourite, Comment


@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash("Wylogowano!", category="success")
    return redirect(url_for("login"))


@login_required
@app.route("/")
def home():
    form = Filter_Films()
    if form.validate_on_submit():
        pass
        # films_number='films_number'
    return render_template("home.html", movies=movies.getPopular(4), form=form)


@app.route("/like_movie/<int:id>", methods=["GET"])
@login_required
def like_movie(id):
    if Favourite.query.filter_by(name=id).first():
        f = Favourite.query.filter_by(name=id)
        f.delete()
        db.session.commit()
        flash("Nie lubisz")
    else:

        fav = Favourite(name=id, user_id=current_user.id)
        db.session.add(fav)
        db.session.commit()
        print('added to favourite')
        flash("Dzieki za glos", category="success")
    return redirect(url_for(f"overview", id=id) )


@app.route("/overview/<int:id>", methods=["GET", "POST"])
@login_required
def overview(id):
    if Favourite.query.filter_by(name=id).first():
        red_heart = False
    else:
        red_heart = True
    form = CommentForm()

    if form.validate_on_submit():
        comment = Comment(comment=form.comment.data, user_id=current_user.id, name=id)
        db.session.add(comment)
        db.session.commit()
        flash("Fajny komentarz, masz stajla", category="success")

    comment_list = []
    for a in Comment.query.filter_by(name=id):
        a.user = User.query.get(a.user_id)
        comment_list.append(a)

    return render_template("overview.html", actor=actor, movies=movies.getPopular(), favs=current_user.favs,
                           cast=movies.getCast(id), movie_overview=movies.getOverview(id), current_user=current_user,
                           form=form,
                           comments=current_user.comments, comment_list=comment_list, id=id, red_heart=red_heart)


@app.route("/signup", methods=['GET', 'POST'])

def sign_up():
    form = SignUpForm()
    if form.validate_on_submit():
        if User.query.filter_by(login=form.login.data).first():
            flash("Podany uzytkownik juz istnieje", category="warning")
        elif User.query.filter_by(email=form.email.data).first():
            flash("Użytkownik o podanym adresie email już istnieje!", category="warning")
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
        if not user:
            flash("Nie znaleziono uzytkownika!", category="info")
        else:
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
@liked_movie_required
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
    return render_template('actor.html', all_actors=movies.getActor(actor_id))


@login_required
@app.route("/random", methods=["GET", "POST"])
def random_movie():
    random_id = random.randint(1, 29949)
    while not movies.isMovieExists(random_id):
        random_id = random.randint(1, 29949)
    return redirect(f"overview/{random_id}")


@app.route("/acceptcookies")
def cookies():
    session["cookies"] = True #zapisuje w sesji przegladarki pare "cookies" i True
    return redirect(url_for("home"))


