from RateFlix.settings import TMDB_API_KEY
from tmdbv3api import TMDb, Discover, Movie   # type: ignore
import json
tmdb = TMDb()
tmdb.api_key = TMDB_API_KEY

def get_movies(sort_by='popularity.desc', genre=None, page=1):
    discover = Discover()
    movies = discover.discover_movies({
        'sort_by': sort_by,
        'page': page,
        'per_page': 50,
        
    })
    
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