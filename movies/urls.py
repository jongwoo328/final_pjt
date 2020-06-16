from django.urls import path
from . import views


app_name = 'movies'

urlpatterns = [
    path('', views.main, name='main'),
    path('index/', views.index, name='index'),
    path('about', views.about, name='about'),
    path('index/search/<str:input_value>/', views.search, name="search"),
    path('index/<str:sort>/', views.index, name='index_sort'),
    path('<int:movie_pk>/', views.detail, name='detail'),
    path('<int:movie_pk>/like/', views.movie_like, name='movie_like'),
    path('<int:movie_pk>/review/create/', views.review_create, name='review_create'),
    path('<int:movie_pk>/review/<int:review_pk>/like/', views.review_like, name='review_like'),
    path('<int:movie_pk>/review/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:movie_pk>/review/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
]