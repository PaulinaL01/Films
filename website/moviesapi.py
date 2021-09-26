import requests
import random

API_KEY = "d086e02925aea6ae99f8b04207381382"


class MoviesAPI:
    def __init__(self):
        self.all_movies = requests.get(
            f"https://api.themoviedb.org/3/movie/popular?api_key={API_KEY}&language=en-US&page=1").json()

    def getPopular(self, count=8):
        self.res = []

        for i, movie in enumerate(self.all_movies['results'][:count]):
            if i % 4 == 0:
                current_list = []
                self.res.append(current_list)
            title = movie['original_title']
            id = movie['id']
            overview = movie['overview']
            popularity = movie['popularity']
            vote_average = movie['vote_average']
            poster = 'https://image.tmdb.org/t/p/w400'+movie['poster_path']
            current_list.append({"id": id, "title": title,"poster": poster, "overview": overview, "popularity": popularity, "vote_average": vote_average})
            random.shuffle(current_list)
        random.shuffle(self.res)

        return self.res

    def getOverview(self,id):

        id = str(id)
        link_overview = 'https://api.themoviedb.org/3/movie/' + id + "?api_key=d086e02925aea6ae99f8b04207381382"
        link_overview = requests.get(link_overview).json()
        if not link_overview['poster_path']:
            pos = 'https://cdn.pixabay.com/photo/2016/08/08/09/17/avatar-1577909_960_720.png'
        else:
            pos = 'https://image.tmdb.org/t/p/w400' + link_overview['poster_path']

        title = link_overview['title']
        overview = link_overview['overview']
        popularity = link_overview['popularity']
        release_date = link_overview ['release_date']

        return {'link_overview' : link_overview, 'pos' : pos, 'title' : title, 'overview' : overview, 'popularity' : popularity, 'release_date' : release_date}



    def getCast(self, id):

        all_credits = requests.get('https://api.themoviedb.org/3/movie/' +
            str(id) + f"/credits?api_key={API_KEY}").json()

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
        fav = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + f"?api_key={API_KEY}"
        all_fav = requests.get(fav).json()
        fav_title = all_fav['original_title']
        fav_poster = 'https://image.tmdb.org/t/p/w400' + all_fav['poster_path']
        return {"id" : movie_id, "poster" : fav_poster, "title" : fav_title}

    def getActor(self, actor_id):
        link_actor = 'https://api.themoviedb.org/3/person/' + str(
            actor_id) + f'?api_key={API_KEY}'
        link_actor = requests.get(link_actor).json()
        detailes_actor = []
        biography_actor = link_actor['biography']
        birthday_actor = link_actor['birthday']
        deathday_actor = link_actor['deathday']
        name_actor = link_actor['name']
        place_of_birth_actor = link_actor['place_of_birth']
        profile_path_actor = 'https://image.tmdb.org/t/p/w400' + str(link_actor['profile_path'])
        detailes_actor.append({'biography_actor' : biography_actor,'birthday_actor': birthday_actor,'deathday_actor': deathday_actor,'name_actor':name_actor,'place_of_birth_actor':place_of_birth_actor,'profile_path_actor': profile_path_actor})

        return detailes_actor

    def isMovieExists(self, movie_id):
        movie_url = 'https://api.themoviedb.org/3/movie/' + str(movie_id) + f"?api_key={API_KEY}"
        movie = requests.get(movie_url).json()
        return "success" not in movie




