from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django import forms
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from .tmdb_utils import get_movies

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

    pass