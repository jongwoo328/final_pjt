from django.db import models
from django.contrib.auth.models import AbstractUser

from community.models import Article, Comment
from movies.models import Movie


class CustomUser(AbstractUser):
    liked_articles = models.ManyToManyField(Article, related_name='liked_users')
    liked_movies = models.ManyToManyField(Movie, related_name='liked_users')
    liked_comments = models.ManyToManyField(Comment, related_name='liked_users')