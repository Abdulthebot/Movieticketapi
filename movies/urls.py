from django.urls import path
from .views import MovieListView, ShowListView

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie-list'),
    path('movies/<int:movie_id>/shows/', ShowListView.as_view(), name='show-list'),
]