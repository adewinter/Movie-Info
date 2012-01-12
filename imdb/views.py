# Create your views here.
from django.contrib.auth.decorators import login_required
from imdb.models import Movie,ScrapeSettings, ScrapeFolder
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.template import RequestContext
from django.core.management import call_command
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout

@login_required
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
    context["c"] = context
    context["is_adewinter"] = request.user
    return render_to_response("imdb/movie_list.html", context, context_instance=RequestContext(request))

def show_all_movie_list(request):
    return movie_list(request,None)

def refresh_movies(request):
    call_command('updatefromimdb')
    return HttpResponse('Refreshing movies now, this may take a few minutes...')



def login(req, template_name="login.html"):
    return django_login(req, **{"template_name" : template_name})


def logout(req, template_name="loggedout.html"):
    return django_logout(req, **{"template_name" : template_name})


def register(req, template_name="register.html"):
    return django_register