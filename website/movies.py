import requests


class Movies:
    def __init__(self):
        self.all_movies = requests.get(
            "https://api.themoviedb.org/3/movie/popular?api_key=d086e02925aea6ae99f8b04207381382&language=en-US&page=1").json()

    def getPopular(self):
        res = []
        for i, movie in enumerate(self.all_movies['results']):
            if i % 4 == 0:
                current_list = []
                res.append(current_list)
            title = movie['original_title']
            poster = 'https://image.tmdb.org/t/p/w400'+movie['poster_path']
            current_list.append({"title" : title, "poster" : poster})
        return res