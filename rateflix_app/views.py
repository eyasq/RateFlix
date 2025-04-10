from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django import forms
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

from django.contrib.auth.models import User
from .tmdb_utils import get_movies, get_movie_details, search_movie, actor_movies
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie, Favorite, Review, Comment
from django.views.decorators.http import require_POST

import json
from mistralai import Mistral

# Create your views here.

def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            #log in user
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "Succesfully Registered!")
            return redirect('home')
        else:
            messages.error(request, "Error registering. Please Try Again")
            return redirect('/register')
    else:
        form = SignUpForm()
    
    return render(request, 'register.html', {"form":form})

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = User.objects.get(username = username)
        except User.DoesNotExist:
            messages.error(request, 'User Does Not Exist')
            return redirect('/login')

        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged In')
            return redirect('/')
        else:
            messages.error(request, 'Invalid Credentials. Please Try Again.')
            return redirect('/login')
    else:
        return render(request, 'login.html')

def home(request):
    #why use TMDB API for our project? there were 3 choices, TMDB, OMDB, and TVMaze. TMDB is the best, as it has built in support for filtering by rating, category, popularity, releasedate, etc, and a generous rate (50reqs/sec). only disadvantage is it doesnt integrate IMDB rating. OMDB does, but has no sorting by popularity or release date, max 1000req/day, less metadata. TV maze api is mostly for TV shows, not movies. So we are using OMDB.
    
    sort_by = request.GET.get('sort_by', 'popularity.desc')
    genre = request.GET.get('genre')
    page = request.GET.get('page', 1)
    try:
        page = int(page)
    except (TypeError, ValueError):
        page = 1
    movies = get_movies(sort_by=sort_by, genre=genre, page=page)
    print(movies)
    context = {
        "movies":movies,
        "next_page":page + 1,
        "current_genre":genre,
        "current_sort":sort_by
        
    }
    return render(request, 'movies.html', context)

def movie_page(request, movie_id):
    movie = get_movie_details(movie_id)
    movie_api_id = movie['details'].id  
    
    
    movie_instance = Movie.objects.filter(api_id=movie_api_id).first()
    if movie_instance:
        reviews = movie_instance.reviews.all()
        comments = movie_instance.comments.all()
    else:
        reviews = []
        comments = []
    
    user_favorite_ids = []
    if request.user.is_authenticated:
        user_favorite_ids = [str(id) for id in request.user.favorites.values_list('movie__api_id', flat=True)]
    is_favorited = str(movie_api_id) in user_favorite_ids
    context = {
        "movie": movie['details'],
        "cast": movie['cast'],
        "reviews": reviews,
        "comments": comments,
        "user_favorite_ids": user_favorite_ids,
        "is_favorited": is_favorited
    }
    return render(request, 'movie_page.html', context)



@login_required
def add_to_favorites(request):
    if request.method == 'POST':
        try:
            # Parse the request body and handle potential JSON decode errors
            data = json.loads(request.body.decode('utf-8'))
            
            api_id = data.get('api_id')
            title = data.get('title')
            poster_url = data.get('poster_url')

            # Add debug print to verify data
            print(f"Adding to favorites: {api_id}, {title}")
            
            # Ensure api_id is the correct type
            if api_id:
                movie, created = Movie.objects.get_or_create(
                    api_id=api_id,
                    defaults={
                        'title': title,
                        'poster_url': poster_url
                    }
                )
                
                favorite_exists = Favorite.objects.filter(user=request.user, movie=movie).exists()
                
                if favorite_exists:
                    # Remove from favorites
                    Favorite.objects.filter(user=request.user, movie=movie).delete()
                    return JsonResponse({'status': 'removed', 'message': 'Movie removed from favorites'})
                else:
                    # Add to favorites
                    Favorite.objects.create(user=request.user, movie=movie)
                    return JsonResponse({'status': 'success', 'message': 'Movie added to favorites'})
            else:
                return JsonResponse({'status': 'error', 'error': 'Missing movie ID'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'status': 'error', 'error': 'Invalid JSON in request body'}, status=400)
        except Exception as e:
            print(f"Error in add_to_favorites: {str(e)}")
            return JsonResponse({'status': 'error', 'error': str(e)}, status=500)
    
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)

@login_required
@require_POST
def submit_review(request):
    try:
        data = json.loads(request.body)
        review_text = data.get('review')
        movie_id = data.get('movie_id')
        rating = data.get('rating')

        movie_data = get_movie_details(movie_id)
        details = movie_data['details']
        title =  details.get('title')
        poster_path = details.get('poster_path')

        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}" if poster_path else None

        movie_instance, created = Movie.objects.get_or_create(
            api_id=movie_id,
            defaults={
                'title': title,
                'poster_url': poster_url
            }
        )

        Review.objects.create(
            user=request.user,
            movie=movie_instance,
            body=review_text,
            rating=rating,
        )

        return JsonResponse({'status': 'success'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=400)
    
@login_required
def delete_review(request, review_id):
    review = Review.objects.filter(id = review_id).first()
    movie = review.movie
    if request.user == review.user:
        review.delete()
        messages.success(request, 'Review succesfully deleted')
        return redirect(f'/movies/{movie.api_id}')
    


@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.filter(id = comment_id).first()
    movie = comment.movie
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment succesfully deleted')
        return redirect(f'/movies/{movie.api_id}')
    


@require_POST
@login_required
def submit_comment(request):
    try:
        data = json.loads(request.body)
        comment_text = data.get('comment')
        movie_id = data.get('movie_id')
        movie_data = get_movie_details(movie_id)
        title = movie_data['details'].get('title')
        poster_url = movie_data['details'].get('poster_url')
        movie_instance, created = Movie.objects.get_or_create(
            api_id = movie_id,
            defaults={
                'title':title,
                'poster_url':poster_url
            }
        )
        comment = Comment.objects.create(
            user = request.user,
            movie = movie_instance,
            body = comment_text
        )
        return JsonResponse({'status':'success'})
    except Exception as e:
        return JsonResponse({'status':'Comment submission failed', 'error':str(e)}, status=400)
    


@login_required
def logout_user(request):
    logout(request)
    messages.success(request, 'Successfully logged out')
    return redirect('/')

def profile(request):
    reviewed_movies = Movie.objects.filter(reviews__user=request.user).distinct()
    favorited_movies = Movie.objects.filter(favorited_by__user=request.user).distinct()
    context={
        'user':request.user,
        'movies':reviewed_movies,
        'favorites':favorited_movies
    }
    return render(request, 'profile.html',context)

def other_profile_(request, profile_id):
    user = request.user
    other = get_object_or_404(User, id = profile_id)
    your_reviewed_movies = Movie.objects.filter(reviews__user=user).distinct()
    other_reviewed_movies = Movie.objects.filter(reviews__user=other).distinct()
    your_favorited_movies = Movie.objects.filter(favorited_by__user=user).distinct()
    other_favorited_movies = Movie.objects.filter(favorited_by__user=other).distinct()
    shared_favorites = your_favorited_movies.filter(id__in=other_favorited_movies)
    if your_reviewed_movies.exists() or other_favorited_movies.exists():
        affinity = int((shared_favorites.count() / max(your_reviewed_movies.count(), other_favorited_movies.count())) * 100)
    else:
        affinity = 0
    context = {
        "user":request.user,
        "user_movies":your_reviewed_movies,
        "user_favorites":your_favorited_movies,
        "other":other,
        "other_movies":other_reviewed_movies,
        "other_favorites":other_favorited_movies,
        "affinity":affinity
    }
    return render(request, 'other_profile.html', context)

def delete_review(request,review_id):
    review = Review.objects.get(id = review_id)
    movie = review.movie
    movie_res = search_movie(movie.title)
    if request.user == review.user:
        review.delete()
    else:
        messages.error(request, "You are not authorized to delete this review")
        return redirect('/')
    return redirect(f'/movies/{movie_res[0].id}')
@require_POST
@login_required
def recommend(request):
    try:
        
        user_id = request.POST.get('data')
        user = User.objects.get(id=user_id)
        
        try:
            user_favorites = list(user.favorites.all().values_list('movie__title', flat=True))
            print(f"User favorites: {user_favorites}")
        except Exception as e:
            print(f"Error fetching favorites: {str(e)}")
            user_favorites = []
        
        try:
            user_reviews = user.reviews.all()
            ratings = []
            for review in user_reviews:
                ratings.append({
                    "title": review.movie.title,
                    "rating": review.rating,
                })
            print(f"User ratings: {ratings}")
        except Exception as e:
            print(f"Error fetching reviews: {str(e)}")
            ratings = []
            
        user_data = {
            "username": user.username,
            "favorites": user_favorites,
            "ratings": ratings
        }
        
        prompt = f"""
        Recommend 5 movies based on these user preferences:
        Favorites: {user_data['favorites']}
        Ratings: {user_data['ratings']}

        Rules:
        - Suggest diverse genres but prioritize similar vibes.
        - Avoid movies the user rated poorly.
        - Format as a bulleted list with 1-sentence explanations.
        """
        
        api_key = os.getenv('MISTRAL_API_KEY')        
        model = "mistral-large-latest"
        client = Mistral(api_key=api_key)
        
        try:
            print("Sending request to Mistral API")
            # Add a timeout to prevent hanging
            chat_response = client.chat.complete(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a movie recommendation engine."},  
                    {"role": "user", "content": prompt}, 
                ],
            )
            ai_response = chat_response.choices[0].message.content
            
            return JsonResponse({
                "status": "success",
                "recommendations": ai_response
            })
        except Exception as e:
            print(f"Error calling Mistral API: {str(e)}")
            return JsonResponse({
                "status": "error",
                "message": f"AI service error: {str(e)}"
            }, status=500)
        
   
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        return JsonResponse({
            "status": "error",
            "message": f"Server error: {str(e)}"
        }, status=500)
    
def actors_movies(request, actor_id):
    _credits = actor_movies(actor_id)
    context = {
        "actor": _credits.get('actor_details'),
        "movies":_credits.get('movie_credits')
    }
    print(_credits['actor_details'])
    return render(request, 'actorsmovies.html', context)

def about(request):
    return render (request,'about.html')
def search(request):
    if request.method == 'POST':
        query = request.POST.get('title')
        if query:
            results = search_movie(query)  # This uses your TMDb utility
            return render(request, 'search_results.html', {'query': query, 'results': results})
        else:
            messages.error(request, "Please enter a search query.")
            return redirect('/')
    return redirect('/')
