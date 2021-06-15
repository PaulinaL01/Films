import requests
from flask import Flask, render_template
from website.movies import Movies

app = Flask(__name__)


@app.route("/")
def home():
    title = Movies().getMovies()
    poster = Movies().getMovies()
    return render_template("home.html", title= title, poster= poster)

