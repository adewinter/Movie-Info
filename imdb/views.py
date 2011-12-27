# Create your views here.
from imdb.models import Movie,ScrapeSettings, ScrapeFolder
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden
from django.template import RequestContext

def movie_list(request):
    movies = Movie.objects.all().order_by('title')
    context = {}
    context["movies"] = movies
    return render_to_response("imdb/movie_list.html", context, context_instance=RequestContext(request))
    