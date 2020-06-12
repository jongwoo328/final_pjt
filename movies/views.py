import datetime

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import Movie, Genre, Review
from .forms import ReviewForm


def main(request):
    '''
    추천 로직
    '''
    pass

def index(request, sort=None):
    if sort == 'rank':
        movies = Movie.objects.order_by('-vote_average')
    elif sort == 'release':
        movies = Movie.objects.order_by('release_date')
    else:
        movies = Movie.objects.order_by('-pk')

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
    else:
        liked = True
    
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
        review.save()
        return redirect('movies:detail', movie_pk)
    context = {
        'movie': movie,
        'form': form,
    }
    return render(request, 'movies:detail', movie_pk)


@login_required
def review_update(request, movie_pk, review_pk):
    review = Review.objects.get(pk=review_pk)

    if request.user != review.author:
        return redirect('movies:detail', movie_pk)
        
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
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
        review.delete()
    return redirect('movies:detail', movie_pk)


@login_required
def movie_like(request, movie_pk, review_pk):
    user = request.user
    review = get_object_or_404(Review, pk=review_pk)

    if review.liked_users.filter(pk=user.pk).exists():
        review.liked_users.remove(user)
        liked = False
    else:
        liked = True
    
    context = {
        'liked': liked,
        'count': review.liked_users.count(),
    }

    return JsonResponse(context)