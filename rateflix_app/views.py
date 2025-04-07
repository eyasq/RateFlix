from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django import forms
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .tmdb_utils import get_movies, get_movie_details
import json
from .models import Movie, Favorite
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
    context ={
        "movie":movie['details'],
        "cast":movie['cast']
    }
    return render(request, 'movie_page.html', context)

@login_required
def add_to_favorites(request):
    try:
        if request.method == 'POST':
            #recieve the data sent by the axios request
            data = json.loads(request.body)
            
            #get the info from the request
            api_id = data.get('api_id')
            title = data.get('title')
            poster_url = data.get('poster_url')
            
            #is there a movie instance in the db? if yes, proceed, if no, create one, then proceed.
            movie, created = Movie.objects.get_or_create(
                api_id=api_id,
                defaults={
                    'title': title,
                    'poster_url': poster_url
                }
            )
            
            #did the user already favorite this, and wants to remove it?
            favorite_exists = Favorite.objects.filter(user=request.user, movie=movie).exists()
            
            if favorite_exists:
                #if he did, remove from favorites
                Favorite.objects.filter(user=request.user, movie=movie).delete()
                return JsonResponse({'status': 'removed', 'message': 'Movie removed from favorites'})
            else:
                #if he didn't, add to favorites
                Favorite.objects.create(user=request.user, movie=movie)
                return JsonResponse({'status': 'success', 'message': 'Movie added to favorites'})
        
        # If not a POST request, return an error
        return JsonResponse({'status': 'error', 'error': 'Invalid request method'}, status=400)
    
    except Exception as e:
        # debugging => dumb mistakes, dumb mistakes
        import traceback
        print(f"Error in add_to_favorites: {str(e)}")
        print(traceback.format_exc())
        
        return JsonResponse({'status': 'error', 'error': str(e)}, status=500)