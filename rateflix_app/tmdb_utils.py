from RateFlix.settings import TMDB_API_KEY
from tmdbv3api import TMDb, Discover  
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
    } for movie in movies]
    
    print(f"Fetched {len(simplified_movies)} movies")
    return simplified_movies


#movies returns adult:false, genre_ids, original language, title, overview, popularity, poster_path, release_date, vote_average,