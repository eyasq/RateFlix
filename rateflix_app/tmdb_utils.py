from RateFlix.settings import TMDB_API_KEY
from tmdbv3api import TMDb, Discover, Movie, Person # type: ignore
import json
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY

def get_movies(sort_by='popularity.desc', genre=None, page=1):
    discover = Discover()
    params = {
        'sort_by':sort_by,
        'page':page,
        'per_page':20,
    }
    if genre:
        params['with_genres'] = genre
    movies = discover.discover_movies(params)
    simplified_movies = [{
        'title': movie.title,
        'rating': movie.vote_average,
        'release_date': movie.release_date,
        'poster_path': movie.poster_path,
        'adult':movie.adult,
        'overview':movie.overview,
        # 'genres':,
        'language':movie.original_language,
        "id":movie.id
    } for movie in movies]
    
    print(f"Fetched {len(simplified_movies)} movies")
    return simplified_movies


#movies returns adult:false, genre_ids, original language, title, overview, popularity, poster_path, release_date, vote_average

def get_movie_details(movie_id):
    movie = Movie()
    details = movie.details(movie_id)
    credits = movie.credits(movie_id)
    cast = list(credits.cast)[:5] #get top 5 actors


    context = {
        "details":details,
        "cast":cast

    }
    return context 

def search_movie(title):
    movie = Movie()
    search_res = movie.search(title)
    return search_res

def actor_movies(actor_id):
    person = Person()
    actor_details = person.details(actor_id)
    actor_credits = person.movie_credits(actor_id) 
    movie_credits = actor_credits.cast #automaticaly sorted by popularity.desc
    credits_dict = {
        "actor_details": actor_details,
        "movie_credits": movie_credits
    }
    return credits_dict