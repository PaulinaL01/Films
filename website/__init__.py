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

@app.route("/overview")
def overview():
    # if request.method == "POST":
    #     selected = request.args.get('movie.title')
    #     print("selected:", selected)
    #     selectedInfo = ""
    #     if selected is not None:
    #         selectedInfo = "hello"
    return render_template("overview.html", movies=movies.getPopular())