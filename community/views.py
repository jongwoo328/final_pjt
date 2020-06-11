from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Article, Comment, Board
from .forms import ArticleForm, CommentForm


def community(request):
    articles = Article.objects.all()
    paginator = Paginator(articles, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    print(page_obj)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'community/index.html', context)

@login_required
def create_article(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            return redirect('community:detail', article.pk)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)

@login_required
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    form = CommentForm()
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'community/detail.html', context)

def update_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article = form.save()
            return redirect('community:detail', article_pk)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)

def delete_article(request, article_pk):
    pass

def create_comment(request, article_pk):
    pass

def update_comment(request, article_pk, comment_pk):
    pass

def delete_comment(request, article_pk, comment_pk):
    pass