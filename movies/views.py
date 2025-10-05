from rest_framework import generics
from .models import Movie, Show
from .serializers import MovieSerializer, ShowSerializer
from django.shortcuts import get_object_or_404

class MovieListView(generics.ListAPIView):
    """
    API view to retrieve a list of all available movies.
    """
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
    permission_classes = [] # Publicly accessible

class ShowListView(generics.ListAPIView):
    """
    API view to retrieve all shows scheduled for a specific movie.
    """
    serializer_class = ShowSerializer
    permission_classes = [] # Publicly accessible

    # The queryset is dynamically filtered based on the movie ID in the URL[cite: 148].
    def get_queryset(self):
        movie = get_object_or_404(Movie, pk=self.kwargs['movie_id'])
        return Show.objects.filter(movie=movie)