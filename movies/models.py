from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


MAX_RANK = 10

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'

class Movie(models.Model):
    title = models.CharField(max_length=100)
    original_title = models.CharField(max_length=100)
    release_date = models.DateField()
    popularity = models.FloatField()
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    adult = models.BooleanField()
    overview = models.TextField()
    original_language = models.CharField(max_length=10)
    poster_path = models.CharField(max_length=100, default='')
    backdrop_path = models.CharField(max_length=100, default='')
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return f'{self.title}'

class Review(models.Model):
    rank = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(MAX_RANK)])
    rank_star = models.CharField(max_length=10)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    liked_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_review')

    def __str__(self):
        return f'{self.movie.title} : {self.rank_star}'
    
    def add_vote(self):
        self.movie.vote_count += 1
        vote_average = self.movie.vote_average
        
        self.movie.vote_average = round(((self.movie.vote_count - 1) * vote_average + self.rank) / self.movie.vote_count, 1)
        self.movie.save()

    def delete_vote(self):
        self.movie.vote_count -= 1
        vote_average = self.movie.vote_average

        try:
            self.movie.vote_average = round(((self.movie.vote_count + 1) * vote_average - self.rank) / (self.movie.vote_count), 1)
        except ZeroDivisionError:
            self.movie.vote_average = 0
        
        self.movie.save()
    
    def update_vote(self, before, after):
        self.movie.vote_average = round((self.movie.vote_average * self.movie.vote_count - before + after) / self.movie.vote_count, 1)
        self.movie.save()
        