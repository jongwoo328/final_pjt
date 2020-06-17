import datetime # 날짜 가져오기
import pytz

from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils import timezone

from .models import Article, Comment, Board
from .forms import ArticleForm, CommentForm, AdminArticleForm


NOTICE_BOARD_NAME = '공지사항'
MAX_NOTICE_COUNT = 3

def community(request):
    boards = Board.objects.all()
    notice_board = Board.objects.get(name=NOTICE_BOARD_NAME)
    noticed = notice_board.article_set.order_by('-pk')
    if len(noticed) >= 3:
        noticed = noticed[:3]
    articles = Article.objects.order_by('-pk').exclude(board=notice_board)

    paginator = Paginator(articles, 10)
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    boards = Board.objects.all()
    context = {
        'page_obj': page_obj,
        'nowDate': nowDate,
        'board': None,
        'boards': boards,
        'noticed': noticed,
    }

    return render(request, 'community/index.html', context)


def board(request, board_name=None):
    notice_board = Board.objects.get(name=NOTICE_BOARD_NAME)
    noticed = notice_board.article_set.order_by('-pk')
    if len(noticed) >= 3:
        noticed = noticed[:3]
    if board_name is None:
        board = None
        articles = Article.objects.order_by('-pk').exclude(board=notice_board)
    else:
        board = get_object_or_404(Board, url_name=board_name)
        articles = board.article_set.order_by('-pk')

    paginator = Paginator(articles, 10)
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    boards = Board.objects.all()
    context = {
        'page_obj': page_obj,
        'nowDate': nowDate,
        'now_board': board,
        'boards' : boards,
        'noticed' : noticed,
    }
    return render(request, 'community/index.html', context)


@login_required
def create_article(request, board_name=None):
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminArticleForm(request.POST)
        else:
            form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.author = request.user
            article.board = get_object_or_404(Board, pk=request.POST.get('board')[0])
            article.updated_at = timezone.now()
            article.save()
            return redirect('community:detail', article.pk)
    else:
        board = get_object_or_404(Board, url_name=board_name)
        if board.auth_required and not request.user.is_superuser:
            messages.error(request, '관리자만 접근 가능합니다.')
            #
            if board_name is None:
                board = None
                articles = Article.objects.order_by('-pk')
            else:
                board = get_object_or_404(Board, url_name=board_name)
                articles = board.article_set.all()

            paginator = Paginator(articles, 10)
            nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            boards = Board.objects.all()
            context = {
                'page_obj': page_obj,
                'nowDate': nowDate,
                'now_board': board,
                'boards' : boards,
            }
            return render(request, 'community/index.html', context)
            #
        else:
            if board_name:
                board = Board.objects.get(url_name=board_name)
                if request.user.is_superuser:
                    form = AdminArticleForm(initial={'board': board})
                else:
                    form = ArticleForm(initial={'board': board})
            else:
                if request.user.is_superuser:
                    form = AdminArticleForm()
                else:
                    form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)


@login_required
def detail(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    article.hit()
    comments = article.comment_set.order_by('-pk')
    nowDate = datetime.datetime.now().strftime('%Y-%m-%d')
    form = CommentForm()
    context = {
        'form': form,
        'article': article,
        'comments' : comments,
        'nowDate': nowDate,
    }
    return render(request, 'community/detail.html', context)


@login_required
def update_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    if request.method == 'POST':
        if request.user.is_superuser:
            form = AdminArticleForm(request.POST, instance=article)
        else:
            form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            article.updated_at = timezone.now()
            article = form.save()
            return redirect('community:detail', article_pk)
    else:
        if request.user != article.author:
            return redirect('community:detail', article_pk)
        if request.user.is_superuser:
            form = AdminArticleForm(instance=article)
        else:
            form = ArticleForm(instance=article)
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)


@login_required
def article_like(request, article_pk):
    user = request.user
    article = get_object_or_404(Article, pk=article_pk)

    if article.liked_users.filter(pk=user.pk).exists():
        article.liked_users.remove(user)
        liked = False
    else:
        article.liked_users.add(user)
        liked = True
    
    context = {
        'article_liked': liked,
        'count': article.liked_users.count(),
    }

    return JsonResponse(context)

@login_required
@require_POST
def delete_article(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    url_name = article.board.url_name
    if request.user == article.author:
        article.delete()
        return redirect('community:board', board_name=url_name)
    return redirect('community:detail', article_pk)


@login_required
def create_comment(request, article_pk):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.article = get_object_or_404(Article, pk=article_pk)
        comment.save()
    return redirect('community:detail', article_pk)

@login_required
def update_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)

    if request.user != comment.author:
        return redirect('community:detail', article_pk)
        
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('community:detail', article_pk)
    else:
        form = CommentForm(instance=comment)
    context = {
        'form': form,
    }
    return render(request, 'community/form.html', context)

@login_required
@require_POST
def delete_comment(request, article_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.author:
        comment.delete()
    return redirect('community:detail', article_pk)


@login_required
def comment_like(request, article_pk, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.liked_users.filter(pk=user.pk).exists():
        comment.liked_users.remove(user)
        liked = False
    else:
        comment.liked_users.add(user)
        liked = True
    
    context = {
        'comment_liked': liked,
        'count': comment.liked_users.count(),
    }

    return JsonResponse(context)