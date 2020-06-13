from django.db import models
from django.contrib.auth.models import AbstractUser

from community.models import Article, Comment
from movies.models import Movie


MAX_RECENTS = 3

class CustomUser(AbstractUser):
    liked_articles = models.ManyToManyField(Article, related_name='liked_users')
    liked_movies = models.ManyToManyField(Movie, related_name='liked_users')
    liked_comments = models.ManyToManyField(Comment, related_name='liked_users')

    # 본인 데이터
    # 연도별 ..
    liked_under60 = models.IntegerField(default=0)
    liked_1960 = models.IntegerField(default=0)
    liked_1970 = models.IntegerField(default=0)
    liked_1980 = models.IntegerField(default=0)
    liked_1990 = models.IntegerField(default=0)
    liked_2000 = models.IntegerField(default=0)
    liked_2010 = models.IntegerField(default=0)
    liked_2020 = models.IntegerField(default=0)

    
    # 장르별 ..
    liked_adventure = models.IntegerField(default=0)
    liked_fantasy = models.IntegerField(default=0)
    liked_animation = models.IntegerField(default=0)
    liked_drama = models.IntegerField(default=0)
    liked_horror = models.IntegerField(default=0)
    liked_action = models.IntegerField(default=0)
    liked_comedy = models.IntegerField(default=0)
    liked_history = models.IntegerField(default=0)
    liked_western = models.IntegerField(default=0)
    liked_thriller = models.IntegerField(default=0)
    liked_crime = models.IntegerField(default=0)
    liked_documentary = models.IntegerField(default=0)
    liked_sciencefiction = models.IntegerField(default=0)
    liked_mystery = models.IntegerField(default=0)
    liked_music = models.IntegerField(default=0)
    liked_romance = models.IntegerField(default=0)
    liked_family = models.IntegerField(default=0)
    liked_war = models.IntegerField(default=0)
    liked_tvmovie = models.IntegerField(default=0)

    liked_recents = models.CharField(max_length=50, default='')

    def liked(self, movie):
        year = movie.release_date.year
        if year < 1960:
            self.liked_under60 += 1
        elif year < 1970:
            self.liked_1960 += 1
        elif year < 1980:
            self.liked_1970 += 1
        elif year < 1990:
            self.liked_1980 += 1
        elif year < 2000:
            self.liked_1990 += 1
        elif year < 2010:
            self.liked_2000 += 1
        elif year < 2020:
            self.liked_2010 += 1
        else:
            self.liked_2020 += 1
        
        for genre in movie.genres.all():
            attrname = f'liked_{"".join(genre.name.lower().split())}'
            value = getattr(self, attrname)
            setattr(self,attrname, value + 1)

        recents_data = self.liked_recents.split()

        if len(recents_data) == MAX_RECENTS:
            recents_data.pop(0)
        recents_data.append(str(movie.pk))

        self.liked_recents = ' '.join(recents_data)
        self.save()
    
    def disliked(self, movie):
        year = movie.release_date.year
        if year < 1960:
            self.liked_under60 -= 1
        elif year < 1970:
            self.liked_1960 -= 1
        elif year < 1980:
            self.liked_1970 -= 1
        elif year < 1990:
            self.liked_1980 -= 1
        elif year < 2000:
            self.liked_1990 -= 1
        elif year < 2010:
            self.liked_2000 -= 1
        elif year < 2020:
            self.liked_2010 -= 1
        else:
            self.liked_2020 -= 1
        
        for genre in movie.genres.all():
            attrname = f'liked_{"".join(genre.name.lower().split())}'
            value = getattr(self, attrname)
            setattr(self,attrname, value - 1)
        
        recents_data = self.liked_recents.split()

        if str(movie.pk) in recents_data:
            recents_data.remove(str(movie.pk))

        self.liked_recents = ' '.join(recents_data)
        self.save()