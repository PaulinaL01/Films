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

    def getCast(self, id):

        all_credits = requests.get('https://api.themoviedb.org/3/movie/' +
            id + "/credits?api_key=d086e02925aea6ae99f8b04207381382").json()

        full_cast = all_credits['cast']

        actors = []
        for i, actor in enumerate(all_credits['cast']):
            actor_name = actor['name']
            actor_pic = 'https://image.tmdb.org/t/p/w400' + str(actor['profile_path'])
            if actor['profile_path'] == None:
                actor_pic = 'https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png'
            actor_role = actor['character']
            actor_id = actor['id']
            actors.append({"id" : actor_id, "name" : actor_name, "pic" : actor_pic, "role" : actor_role, })

        return actors


    def getMovieDetails(self, movie_id):
        pass