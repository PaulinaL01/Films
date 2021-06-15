import requests


class Movies:
    def __init__(self):
        self.all_movies = requests.get(
            "https://api.themoviedb.org/3/movie/popular?api_key=d086e02925aea6ae99f8b04207381382&language=en-US&page=1").json()

    def getMovies(self):
        for movie in self.all_movies['results']:
            title = movie['original_title']
            poster = 'https://image.tmdb.org/t/p/w400'+movie['poster_path']

            return title, poster