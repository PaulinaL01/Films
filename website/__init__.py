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
    print(link_overview)
    pos='https://image.tmdb.org/t/p/w400'+link_overview['poster_path']
    credits = 'https://api.themoviedb.org/3/movie/' + id + "/credits?api_key=d086e02925aea6ae99f8b04207381382"
    all_credits = requests.get(credits).json()


    full_cast = all_credits['cast']
    cast_length = len(full_cast)
    print(full_cast,cast_length)


    #
    # res = []
    # for i, movie in range(cast_length):
    #     if i % 3 == 0:
    #         current_list = []
    #         res.append(current_list)
    #     actor_name = movie['name']
    #     actor_role = movie['character']
    #     actor_pic = 'https://image.tmdb.org/t/p/w400' + movie['profile_path']
    #     current_list.append({"actor_name": actor_name, "actor_role": actor_role, "actor_pic": actor_pic})
    #     return res



    return render_template("overview.html", movies=movies.getPopular(), link_overview=link_overview, pos=pos, all_credits=all_credits, full_cast=full_cast)