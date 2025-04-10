"""
URL configuration for RateFlix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path('register', views.register_user, name='register'),
    path('login', views.login_user, name='login'),
    path('', views.home, name='home'),
    path('profile/',views.profile,name='profile'),
    path('profile/<int:profile_id>',views.other_profile_,name='other_profile'),
    path('movies/<int:movie_id>', views.movie_page, name='movie_page'),
    path('add_to_favorites/', views.add_to_favorites, name='add_to_favorites'),
    path('submit_review/', views.submit_review, name='submit_review'),
    path('submit_comment/', views.submit_comment, name='submit_comment'),
    path('comments/delete/<int:comment_id>', views.delete_comment, name='delete_comment'),
    path('reviews/delete/<int:review_id>', views.delete_review, name='delete_review'),
    path('logout', views.logout_user, name='logout'),
    path('search', views.search, name='search')


]
