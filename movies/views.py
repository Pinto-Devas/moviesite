from django.http import HttpResponse
from .temp_data import movie_data

def detail_movie(request, movie_id):
  movie = movie_data[movie_id - 1]
  return HttpResponse(
    f'Detalhes do filme {movie["name"]} ({movie["release_year"]})')