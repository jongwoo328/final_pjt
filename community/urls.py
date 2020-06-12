from django.urls import path
from . import views


app_name = 'community'

urlpatterns = [
    path('', views.community, name='community'),
    path('create/', views.create_article, name='create_article_noboard'),
    path('<int:article_pk>/', views.detail, name='detail'),
    path('<int:article_pk>/like/', views.article_like, name='article_like'),
    path('<int:article_pk>/update/', views.update_article, name='update_article'),
    path('<int:article_pk>/delete/', views.delete_article, name='delete_article'),
    path('<int:article_pk>/comment/create/', views.create_comment, name='create_comment'),
    path('<int:article_pk>/comment/<int:comment_pk>/update/', views.update_comment, name='update_comment'),
    path('<int:article_pk>/comment/<int:comment_pk>/delete/', views.delete_comment, name='delete_comment'),
    path('<int:article_pk>/comment/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
    path('<str:board_name>/', views.board, name='board'),
    path('<str:board_name>/create/', views.create_article, name='create_article'),
]