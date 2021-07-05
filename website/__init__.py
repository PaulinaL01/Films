import requests
from flask import Flask, render_template, request
from werkzeug.utils import redirect

from website.movies import Movies

app = Flask(__name__)
movies = Movies()

@app.route("/")
def home():
    return render_template("home.html", movies=movies.getPopular())

# @app.route("/process", methods = ['POST', 'GET'])
# def process():
#     if request.method == 'POST':
#         title = request.args.get['movie.title']
#         return redirect(f"/overview/{title}")


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

    for i,actor in enumerate(all_credits['cast']):
        actor_name = actor['name']
        actor_pic = 'https://image.tmdb.org/t/p/w400' + str(actor['profile_path'])
        actor_role = actor['character']
        print(actor_name)

    return render_template("overview.html", movies=movies.getPopular(), link_overview=link_overview, pos=pos, all_credits=all_credits, full_cast=full_cast, name_list=name_list, role_list=role_list, pic_list=pic_list, cast_length=cast_length)