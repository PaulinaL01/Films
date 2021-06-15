import requests
from flask import Flask, render_template
from website.movies import Movies

app = Flask(__name__)
movies = Movies()


@app.route("/")
def home():
    return render_template("home.html", movies=movies.getPopular())

