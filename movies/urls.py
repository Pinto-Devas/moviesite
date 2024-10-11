from django.urls import path

from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.MovieListView.as_view(), name='index'),
    path('search/', views.search_movies, name='search'),
    path('create/', views.create_movie, name='create'),
    path('<int:movie_id>/', views.detail_movie, name='detail'),
    path('update/<int:movie_id>/', views.update_movie, name='update'),
    path('delete/<int:movie_id>/', views.delete_movie, name='delete'),
    path('<int:movie_id>/review/', views.create_review, name='review'),
    path('lists/', views.ListListView.as_view(), name='lists'),
    path('lists/create', views.ListCreateView.as_view(), name='create-list'),
]
