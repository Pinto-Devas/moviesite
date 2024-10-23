from django.forms import ModelForm
from .models import Movie
from django.forms import ModelForm
from .models import Movie, Review
from django.forms import ModelForm
from .models import Movie, Review, Provider

class MovieForm(ModelForm):
  class Meta:
    model = Movie
    fields = [
      'name',
      'release_year',
      'poster_url',
    ]
    labels = {
      'name': 'Título',
      'release_year': 'Data de Lançamento',
      'poster_url': 'URL do Poster',
    }

class ReviewForm(ModelForm):
  class Meta:
    model = Review
    fields = [
      'text',
    ]
    labels = {
      'text': 'Resenha',
    }

class ProviderForm(ModelForm):
  class Meta:
    model = Provider
    fields = [
      'service',
      'has_flat_price',
      'price',
    ]
    labels = {
      'service': 'Serviço de Streaming',
      'has_flat_price': 'FLAT?',
      'price': 'Preço',
    } 
