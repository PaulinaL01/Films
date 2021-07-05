import requests
from flask import Flask, render_template, request, url_for, redirect
from werkzeug.security import check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash

from website.movies import Movies

app = Flask(__name__)
movies = Movies()

@app.route("/")
def home():
    return render_template("home.html", movies=movies.getPopular())
@app.route("/overview/<int:id>")
def overview(id):
    id = str(id)
    link_overview = 'https://api.themoviedb.org/3/movie/'+ id + "?api_key=d086e02925aea6ae99f8b04207381382"
    link_overview = requests.get(link_overview).json()

    pos='https://image.tmdb.org/t/p/w400'+link_overview['poster_path']
    credits = 'https://api.themoviedb.org/3/movie/' + id + "/credits?api_key=d086e02925aea6ae99f8b04207381382"
    all_credits = requests.get(credits).json()


    full_cast = all_credits['cast']
    cast_length = len(full_cast)
    name_list = []
    pic_list = []
    role_list = []
    for i,actor in enumerate(all_credits['cast']):
        actor_name = actor['name']
        actor_pic = 'https://image.tmdb.org/t/p/w400' + str(actor['profile_path'])
        actor_role = actor['character']
        name_list.append(actor_name)
        pic_list.append(actor_pic)
        role_list.append(actor_role)
    return render_template("overview.html", movies=movies.getPopular(), link_overview=link_overview, pos=pos, all_credits=all_credits, full_cast=full_cast, name_list=name_list, role_list=role_list, pic_list=pic_list, cast_length=cast_length)
@app.route("/login")
def login():
    print(request.args)
    log = request.args.get("login", None)
    password = request.args.get("password", None)
    return render_template("login.html")
@app.route("/signup", methods=['GET', 'POST'])
def sign_up():
    message = ""
    if request.method == "POST": #wejscie przez POST oznacza ze uzytkownik chce sie zarejestowac (kliknal w submit w formularzu)
        #TODO: dodac walidacje danych
        login = request.form.get("login", None)
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        password2 = request.form.get("password2", None)

        validation = Validation(password=password, password2=password2)

        if not validation.passwordsEquals():
            message += "Oba hasla sa rozne! "
        if not validation.passwordHasUpperLetter():
            message += "Haslo nie zawiera duzej literki "
        if not validation.passwordHasDigit():
            message += "Haslo nie zawiera cyfry "
        if not validation.long():
            message += "Haslo powinno zawiera przynajmniej 8 znakow "
        if User.query.filter_by(login=login).first():
            message += "Podany uzytkownik juz istnieje "

        if message == "":
            message = "Stworzono!"
            user = User(login=login, email=email, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()

    return render_template("sign_up.html", message=message, current_user=current_user)