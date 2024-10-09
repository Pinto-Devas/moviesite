from django.http import HttpResponse
from .temp_data import movie_data
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie
from django.shortcuts import render, get_object_or_404
from django.views import generic

def detail_movie(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  context = {'movie': movie}
  return render(request, 'movies/detail.html', context)

class MovieListView(generic.ListView):
  model = Movie
  template_name = 'movies/index.html'

def search_movies(request):
  context = {}
  if request.GET.get('query', False):
    search_term = request.GET['query'].lower()
    movie_list = Movie.objects.filter(name__icontains=search_term)
    context = {"movie_list": movie_list}
  return render(request, 'movies/search.html', context)

def create_movie(request):
  if request.method == 'POST':
    movie_name = request.POST['name']
    movie_release_year = request.POST['release_year']
    movie_poster_url = request.POST['poster_url']
    movie = Movie(name=movie_name,
                  release_year=movie_release_year,
                  poster_url=movie_poster_url)
    movie.save()
    return HttpResponseRedirect(reverse('movies:detail', args=(movie.id, )))
  else:
    return render(request, 'movies/create.html', {})
  
def update_movie(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)

  if request.method == "POST":
    movie.name = request.POST['name']
    movie.release_year = request.POST['release_year']
    movie.poster_url = request.POST['poster_url']
    movie.save()
    return HttpResponseRedirect(reverse('movies:detail', args=(movie.id, )))

  context = {'movie': movie}
  return render(request, 'movies/update.html', context)


def delete_movie(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)

  if request.method == "POST":
    movie.delete()
    return HttpResponseRedirect(reverse('movies:index'))

  context = {'movie': movie}
  return render(request, 'movies/delete.html', context)