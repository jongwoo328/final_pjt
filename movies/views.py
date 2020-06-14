import datetime
import random

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Movie, Genre, Review, MAX_RANK
from .forms import ReviewForm


ALL_MOVIE_COUNT = 2000
RANDOM_MOVIE_COUNT = 10


def start(request) : 
    return redirect('movies:main')


def recommend(recents):
    '''
    최근 좋아요 한 영화 기준으로 추천
    1. 장르
    2. 제목
    '''
    # 1.
    # 가장 많이 중복된 장르 추출
    # -> favorite_genres : list
    # 2.
    # 유사한 제목으로 추출
    # 키워드는 보통 앞에 있을거라고 생각하고

    genre_data = dict()
    favorite_genres = []
    keywords = []
    for movie in recents:
        # 1.
        for genre in movie.genres.iterator():
            genre_data[genre] = genre_data.get(genre, 0) + 1
        
        # 2.
        keywords.append(movie.title.split()[0])

    maxcount = 0
    for genre, count in genre_data.items():
        if count > maxcount:
            maxcount = count
            favorite_genres = [genre]
        elif count == maxcount:
            favorite_genres.append(genre)

    genre_recommends = []
    for genre in favorite_genres:
        genre_recommends += random.sample(tuple(genre.movies.all()), RANDOM_MOVIE_COUNT)
    
    # 장르로 뽑은 결과 
    # -> genre_recommends : list
    genre_recommends = Movie.objects.filter(pk__in=[movie.id for movie in random.sample(genre_recommends, RANDOM_MOVIE_COUNT//2)])
    
    # keyword_recommends_with_pk -> keyword로 추출한 영화의 pk list
    # recents_with_pk -> 입력 영화의 pk map
    keyword_recommends_with_pk = []
    for keyword in keywords:
        keyword_recommends_with_pk += map(lambda movie: movie.pk ,Movie.objects.filter(title__icontains=keyword).iterator())
    recents_with_pk = map(lambda movie: movie.pk, recents.iterator())

    # 추출결과에서 이미 추천된 영화는 제외
    keyword_recommends = \
        Movie.objects.filter(pk__in=keyword_recommends_with_pk)\
        .exclude(pk__in=recents_with_pk)

    result = keyword_recommends | genre_recommends
    
    return result

def main(request):
    # 랜덤 영화
    random_movies = Movie.objects.filter(
        pk__in=list(random.sample(
            range(1, ALL_MOVIE_COUNT+1), RANDOM_MOVIE_COUNT
            ))
        )
    
    # 최근 기록
    # 최근 기록은 user.recents() << method로 사용할것
    if request.user.is_authenticated:
        recents = request.user.recents()
        if recents:
            recommends = recommend(recents)
        else:
            recommends = Movie.objects.none()
        is_logged_in = True
    else:
        recommends = Movie.objects.none()
        is_logged_in = False

    context = {
        'movies' : random_movies,
        'recommends': recommends,
        'is_logged_in': is_logged_in,
    }
    return render(request, 'movies/main.html', context)

def index(request, sort=None):
    if sort == 'rank':
        movies = Movie.objects.order_by('-vote_average').filter(release_date__lte=datetime.datetime.now())
    elif sort == 'release':
        movies = Movie.objects.order_by('-release_date').filter(release_date__lte=datetime.datetime.now())
    else:
        movies = Movie.objects.order_by('-pk').filter(release_date__lte=datetime.datetime.now())

    paginator = Paginator(movies, 12)
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'nowDate': nowDate,
    }
    return render(request, 'movies/index.html', context)

@login_required
def detail(request, movie_pk):
    movie = Movie.objects.get(pk=movie_pk)
    reviews = movie.review_set.order_by('-pk')
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    form = ReviewForm()
    context = {
        'movie': movie,
        'form': form,
        'reviews': reviews,
    }
    return render(request, 'movies/detail.html', context)

@login_required
def movie_like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)

    if movie.liked_users.filter(pk=user.pk).exists():
        movie.liked_users.remove(user)
        liked = False
        user.disliked(movie)
    else:
        movie.liked_users.add(user)
        liked = True
        user.liked(movie)
    context = {
        'liked': liked,
        'count': movie.liked_users.count(),
    }

    return JsonResponse(context)


@login_required
@require_POST
def review_create(request, movie_pk):
    form = ReviewForm(request.POST)
    movie = Movie.objects.get(pk=movie_pk)
    if form.is_valid():
        review = form.save(commit=False)
        review.author = request.user
        review.movie = movie
        review.rank_star =  ('★' * review.rank) + ('☆' * (MAX_RANK - review.rank))
        review.save()
        review.add_vote()
        return redirect('movies:detail', movie_pk)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies/detail.html', movie_pk)


@login_required
def review_update(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    before = review.rank
    if request.user != review.author:
        return redirect('movies:detail', movie_pk)
        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            new_review = form.save()
            after = new_review.rank
            new_review.update_vote(before, after)
            return redirect('movies:detail', movie_pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
    }
    return render(request, 'movies/form.html', context)

@login_required
@require_POST
def review_delete(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)
    if request.user == review.author:
        review.delete_vote()
        review.delete()
    return redirect('movies:detail', movie_pk)


@login_required
def review_like(request, movie_pk, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)

    if review.liked_users.filter(pk=user.pk).exists():
        review.liked_users.remove(user)
        liked = False
    else:
        review.liked_users.add(user)
        liked = True
    
    context = {
        'liked': liked,
        'count': review.liked_users.count(),
    }

    return JsonResponse(context)