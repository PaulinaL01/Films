import random
from functools import wraps
from .dekoratory import liked_movie_required, not_log_in
from flask_dance.contrib.github import github
from flask_avatars import Avatars
from numpy._distributor_init import basedir
import requests
from flask import Flask, render_template, request, url_for, redirect, flash, session, send_from_directory,render_template_string,jsonify
from flask_login import login_required, login_user, logout_user, current_user
from . import app, db, User, movies, avatars,mail
from werkzeug.security import generate_password_hash
from .forms import LoginForm, SignUpForm, CommentForm, FilterFilms
from .models import Favourite, Comment
from flask_mail import Message
from .utils import create_code


@login_required
@app.route("/logout")
def logout():
    logout_user()
    flash("Wylogowano!", category="success")
    return redirect(url_for("login"))


@login_required
@app.route("/", methods=["GET", "POST"])
def home():
    form = FilterFilms()
    selected = 8
    selected_list = [4, 8, 12, 16]
    if form.validate_on_submit():
        selected = form.films_number.data

    return render_template("home.html", movies=movies.getPopular(selected), selected=selected, form=form, selected_list=selected_list)


@login_required
@app.route("/api/popular/<int:count>", methods=["GET", "POST"])
def popular_movies(count):
    return render_template("popular.html", movies=movies.getPopular(count))


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
                        password=generate_password_hash(form.password1.data),
                        confirm_code=create_code(64))
            db.session.add(user)
            db.session.commit()
            msg = Message("Email confirmation", sender=("Flask Project", "flaskproject2@gmail.com"),
                          recipients=[user.email])
            with open("website/templates/email_confirmation.html", "r", encoding="utf-8") as f:
                msg.html = render_template_string(f.read(), code=user.confirm_code)
                mail.send(msg)
            flash("Account created! Confirm email adress", category="success")
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
        elif not user.confirmed_email:
            flash("Nie potwierdzono adresu email", category="danger")
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

@app.route("/github_login")
def github_login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    else:
        resp = github.get("/user")
        print(resp)
        print(resp.json())
        name = resp.json()["login"]
        email = resp.json()["email"]
        user = User.query.filter_by(login=name).first()
        if not user:
            user = User(login=name, email=email,
                        password=generate_password_hash("1234567"),
                        is_github_account=True,
                        confirmed_email=True)
            db.session.add(user)
            db.session.commit()
            user = User.query.filter_by(login=name).first()
        login_user(user)

        if not user.is_github_account:
            flash("Konto po podanej nazwie juz istnieje i nie jest powiazane z github-em", category="warning")
            return redirect(url_for("login"))

        return redirect(url_for("home"))

@app.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(app.config['AVATARS_SAVE_PATH'], filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files.get('file')
        raw_filename = avatars.save_avatar(f)
        session['raw_filename'] = raw_filename  # you will need to store this filename in database in reality
        return redirect(url_for('crop'))
    return render_template('upload.html')

@app.route('/crop', methods=['GET', 'POST'])
def crop():
    if request.method == 'POST':
        x = request.form.get('x')
        y = request.form.get('y')
        w = request.form.get('w')
        h = request.form.get('h')
        filenames = avatars.crop_avatar(session['raw_filename'], x, y, w, h)
        url_s = url_for('get_avatar', filename=filenames[0])
        url_m = url_for('get_avatar', filename=filenames[1])
        url_l = url_for('get_avatar', filename=filenames[2])
        return render_template('done.html', url_s=url_s, url_m=url_m, url_l=url_l)
    return render_template('crop.html')

@app.route("/register/<code>")
def confirm_email(code):
    user = User.query.filter_by(confirm_code=code).first()
    if not user:
        return "Bad request", 400
    user.confirmed_email = True
    user.confirm_code = None
    db.session.commit()
    flash("Email confirmed", category="success")
    return redirect(url_for("login"))