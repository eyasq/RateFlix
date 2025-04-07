from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django import forms
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .tmdb_utils import get_movies, get_movie_details
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Movie, Favorite, Review, Comment
from django.views.decorators.http import require_POST

import json
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
    movies = get_movies(sort_by=sort_by, genre=genre)
    print(movies)
    context = {
        "movies":movies,
        
    }
    return render(request, 'movies.html', context)

def movie_page(request, movie_id):
    movie = get_movie_details(movie_id)
    print(movie['details'].title, movie['details'].overview)
    print(movie['cast'])
    #to loads reviews, first we have to check if there is a movie instance. if there is not, then there are no reviews. If there is a movie instance, then load all reviews associated with this movie instance.
    # movie_instance = Movie.get_object_or_404 this would break my flow if not found
    movie_instance = Movie.objects.filter(api_id = movie['details'].id).first()
    if movie_instance:
        reviews = movie_instance.reviews
        comments = movie_instance.comments
    else:
        reviews=[]
        comments=[]
    user_favorites = request.user.favorites.values_list('movie__api_id', flat=True) if request.user.is_authenticated else[]
    context ={
        "movie":movie['details'],
        "cast":movie['cast'],
        "reviews":reviews,
        "comments":comments,
        "user_favorites":list(user_favorites)
    }
    return render(request, 'movie_page.html', context)



@login_required
def add_to_favorites(request):
    
    if request.method == 'POST':
        data = json.loads(request.body)
        
        api_id = data.get('api_id')
        title = data.get('title')
        poster_url = data.get('poster_url')
        
        movie, created = Movie.objects.get_or_create(
            api_id=api_id,
            defaults={
                'title': title,
                'poster_url': poster_url
            }
        )
        
        favorite_exists = Favorite.objects.filter(user=request.user, movie=movie).exists()
        
        if favorite_exists:
            Favorite.objects.filter(user=request.user, movie=movie).delete()
            return JsonResponse({'status': 'removed', 'message': 'Movie removed from favorites'})
        else:
            Favorite.objects.create(user=request.user, movie=movie)
            return JsonResponse({'status': 'success', 'message': 'Movie added to favorites'})
    
    return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)

@require_POST
def submit_review(request):
    try:
        data = json.loads(request.body)
        review_text = data.get('review')
        movie_id = data.get('movie_id')
        rating=data.get('rating')
        
        review = Review.objects.create(
            user=request.user,
            movie_id=movie_id,
            body=review_text,
            rating=rating,
        )
        
        return JsonResponse({'status': 'success'})
    
    except Exception as e:
        return JsonResponse({'status': 'error', 'error': str(e)}, status=400)