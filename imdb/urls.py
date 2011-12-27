from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^$','imdb.views.movie_list')
)
  