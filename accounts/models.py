from django.db import models
from django.contrib.auth.models import AbstractUser

from community.models import Article


class CustomUser(AbstractUser):
    liked_articles = models.ManyToManyField(Article, related_name='liked_users')