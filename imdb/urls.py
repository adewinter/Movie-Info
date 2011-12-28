from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^$','imdb.views.movie_list'),
    url(r'^refresh-movies/', 'imdb.views.refresh_movies'),
)
  