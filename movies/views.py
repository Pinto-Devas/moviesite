from django.http import HttpResponse
from .temp_data import movie_data
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Movie
from django.shortcuts import render, get_object_or_404
from django.views import generic
from .models import Movie
from .forms import MovieForm
from .models import Movie, Review
from .forms import MovieForm, ReviewForm
from django.urls import reverse, reverse_lazy
from .models import Movie, Review, List
from .models import Movie, Review, List, Provider
from .forms import MovieForm, ReviewForm, ProviderForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def detail_movie(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  if 'last_viewed' not in request.session:
    request.session['last_viewed'] = []
  request.session['last_viewed'] = [movie_id] + request.session['last_viewed']
  if len(request.session['last_viewed']) > 5:
    request.session['last_viewed'] = request.session['last_viewed'][:-1]
  context = {'movie': movie}
  return render(request, 'movies/detail.html', context)

class MovieListView(generic.ListView):
  model = Movie
  template_name = 'movies/index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    if 'last_viewed' in self.request.session:
      context['last_movies'] = []
      for movie_id in self.request.session['last_viewed']:
        context['last_movies'].append(get_object_or_404(Movie, pk=movie_id))
    return context

def search_movies(request):
  context = {}
  if request.GET.get('query', False):
    search_term = request.GET['query'].lower()
    movie_list = Movie.objects.filter(name__icontains=search_term)
    context = {"movie_list": movie_list}
  return render(request, 'movies/search.html', context)

@login_required
@permission_required('movies.add_movie')
def create_movie(request):
  if request.method == 'POST':
    movie_form = MovieForm(request.POST)
    provider_form = ProviderForm(request.POST)
    if movie_form.is_valid():
      movie = Movie(**movie_form.cleaned_data)
      movie.save()
      if provider_form.is_valid() and provider_form.cleaned_data['service']:
        provider = Provider(movie=movie, **provider_form.cleaned_data)
        provider.save()
      return HttpResponseRedirect(reverse('movies:detail', args=(movie.pk, )))
  else:
    movie_form = MovieForm()
    provider_form = ProviderForm()
  context = {'movie_form': movie_form, 'provider_form': provider_form}
  return render(request, 'movies/create.html', context)

@login_required
@permission_required('movies.change_movie')  
def update_movie(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)

  if request.method == "POST":
    form = MovieForm(request.POST)
    if form.is_valid():
      movie.name = form.cleaned_data['name']
      movie.release_year = form.cleaned_data['release_year']
      movie.poster_url = form.cleaned_data['poster_url']
      movie.save()
      return HttpResponseRedirect(reverse('movies:detail', args=(movie.id, )))
  else:
    form = MovieForm(
      initial={
        'name': movie.name,
        'release_year': movie.release_year,
        'poster_url': movie.poster_url
      })

  context = {'movie': movie, 'form': form}
  return render(request, 'movies/update.html', context)

@login_required
@permission_required('movies.delete_movie')  
def delete_movie(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)

  if request.method == "POST":
    movie.delete()
    return HttpResponseRedirect(reverse('movies:index'))

  context = {'movie': movie}
  return render(request, 'movies/delete.html', context)

def create_review(request, movie_id):
  movie = get_object_or_404(Movie, pk=movie_id)
  if request.method == 'POST':
    form = ReviewForm(request.POST)
    if form.is_valid():
      review_author = request.user
      review_text = form.cleaned_data['text']
      review = Review(author=review_author,
                      text=review_text,
                      movie=movie)
      review.save()
      return HttpResponseRedirect(reverse('movies:detail', args=(movie_id, )))
  else:
    form = ReviewForm()
  context = {'form': form, 'movie': movie}
  return render(request, 'movies/review.html', context)

class ListListView(generic.ListView):
  model = List
  template_name = 'movies/lists.html'

class ListCreateView(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
  model = List
  template_name = 'movies/create_list.html'
  fields = ['name', 'author', 'movies']
  success_url = reverse_lazy('movies:lists')
