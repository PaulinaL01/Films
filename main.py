from flask import Flask, render_template, request
import requests
import json

movies = requests.get("https://api.themoviedb.org/3/movie/popular?api_key=d086e02925aea6ae99f8b04207381382&language=en-US&page=1").json()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html",movies=movies)

app.run(debug=True)