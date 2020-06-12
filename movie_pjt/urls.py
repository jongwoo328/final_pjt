from django.contrib import admin
from django.urls import path, include
from community import views

urlpatterns = [
    path('', views.community),
    path('admin/', admin.site.urls),
    path('movies/', include('movies.urls')),
    path('community/', include('community.urls')),
    path('accounts/', include('accounts.urls')),
]
