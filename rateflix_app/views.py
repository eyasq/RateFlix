from django.shortcuts import redirect, render
from django import forms
from .forms import SignUpForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User

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

