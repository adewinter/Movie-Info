# Create your views here.
from imdb.models import Movie,ScrapeSettings, ScrapeFolder
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.core.management import call_command

def movie_list(request,folder_id):
    context = {}
    if folder_id:
        movies = Movie.objects.filter(folder__id=folder_id).order_by('title')
        name = ScrapeFolder.objects.filter(id=folder_id)[0].folder_name
    else:
        movies = Movie.objects.all().order_by('title')
        name = 'All Folders'
    context["movies"] = movies
    folders = ScrapeFolder.objects.all()
    context["folders"] = folders
    context["num_movies"] = movies.count()

    context["page_title"] = 'Movies from: %s' % name
    return render_to_response("imdb/movie_list.html", context, context_instance=RequestContext(request))

def show_all_movie_list(request):
    return movie_list(request,None)

def refresh_movies(request):
    call_command('updatefromimdb')
    return HttpResponse('Refreshing movies now, this may take a few minutes...')
