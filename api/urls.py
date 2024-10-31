from django.urls import path
from .views import MovieList, MovieDetail, ReviewList, ReviewDetail

urlpatterns = [
  path('movies/<int:pk>/', MovieDetail.as_view()),
  path('movies/', MovieList.as_view()),
  path('reviews/<int:pk>/', ReviewDetail.as_view()),
  path('reviews/', ReviewList.as_view()),
]
