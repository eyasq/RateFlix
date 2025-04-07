from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Movie(models.Model):
    api_id = models.CharField(max_length=50, unique=True) 
    title = models.CharField(max_length=255)
    poster_url = models.URLField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    body = models.TextField()
    rating = models.PositiveSmallIntegerField(blank=True) #1-5 // 1-10
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('user', 'movie') 
    
    
class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='comments')
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='favorited_by')
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'movie') 