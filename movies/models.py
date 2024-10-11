from django.db import models
from django.conf import settings

class Movie(models.Model):
  name = models.CharField(max_length=255)
  release_year = models.IntegerField()
  poster_url = models.URLField(max_length=200, null=True)

  def __str__(self):
    return f'{self.name} ({self.release_year})'

class Review(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
  text = models.CharField(max_length=255)
  likes = models.IntegerField(default=0)
  movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

  def __str__(self):
    return f'"{self.text}" - {self.author.username}'
  
class List(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
  name = models.CharField(max_length=255)
  movies = models.ManyToManyField(Movie)

  def __str__(self):
    return f'{self.name} by {self.author}'
