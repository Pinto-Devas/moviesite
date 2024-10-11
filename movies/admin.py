from django.contrib import admin

from .models import Movie, Review, List

admin.site.register(Movie)
admin.site.register(Review)
admin.site.register(List)