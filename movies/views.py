from django.http import HttpResponse
from .temp_data import movie_data
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

def detail_movie(request, movie_id):
  context = {'movie': movie_data[movie_id - 1]}
  return render(request, 'movies/detail.html', context)

def list_movies(request):
  context = {"movie_list": movie_data}
  return render(request, 'movies/index.html', context)

def search_movies(request):
  context = {}
  if request.GET.get('query', False):
    context = {
      "movie_list": [
        m for m in movie_data
        if request.GET['query'].lower() in m['name'].lower()
      ]
    }
  return render(request, 'movies/search.html', context)

def create_movie(request):
  if request.method == 'POST':
    movie_data.append({
      'name': request.POST['name'],
      'release_year': request.POST['release_year'],
      'poster_url': request.POST['poster_url']
    })
    return HttpResponseRedirect(
      reverse('movies:detail', args=(len(movie_data), )))
  else:
    return render(request, 'movies/create.html', {})