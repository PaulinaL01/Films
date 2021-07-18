import requests

API_KEY = "d086e02925aea6ae99f8b04207381382"


class MoviesAPI:
    def __init__(self):
        self.all_movies = requests.get(
            f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1").json()

    def getPopular(self):
        res = []
        for i, movie in enumerate(self.all_movies['results']):
            if i % 4 == 0:
                current_list = []
                res.append(current_list)
            title = movie['original_title']
            id = movie['id']
            overview = movie['overview']
            popularity = movie['popularity']
            # release_date = movie['release_date']
            vote_average = movie['vote_average']
            poster = 'https://image.tmdb.org/t/p/w400'+movie['poster_path']
            current_list.append({"id" : id, "title" : title, "poster" : poster, "overview" : overview, "popularity" : popularity, "vote_average" : vote_average})
        return res

    def getCast(self, movie_id):
        pass

    def getMovieDetails(self, movie_id):
        pass