from django.conf.urls.defaults import *



urlpatterns = patterns('',
    url(r'^$', 'imdb.views.show_all_movie_list'),
    url(r'^showfolder/(?P<folder_id>\d+)/$','imdb.views.movie_list'),
    url(r'^refresh-movies/$', 'imdb.views.refresh_movies'),
)
  