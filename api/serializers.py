from rest_framework import serializers

from movies.models import Movie, Review

class ReviewSerializer(serializers.ModelSerializer):

  class Meta:
    model = Review
    fields = ['id', 'author', 'text', 'likes', 'movie']

class MovieSerializer(serializers.ModelSerializer):
  review_set = ReviewSerializer(many=True, read_only=True)

  class Meta:
    model = Movie
    fields = ['id', 'name', 'release_year', 'poster_url', 'review_set']