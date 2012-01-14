# Create your views here.
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from imdb.models import Title,ScrapeSettings, ScrapeFolder, CachedTitle
from django.shortcuts import redirect, render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, HttpResponseNotAllowed, HttpResponseNotModified
from django.template import RequestContext
from django.core.management import call_command
from django.contrib.auth.views import login as django_login
from django.contrib.auth.views import logout as django_logout
import json

@login_required
def movie_list(request,folder_id):
    context = {}
    user = request.user
    if folder_id:
        movies = Title.objects.filter(folder__id=folder_id).order_by('title')
        name = ScrapeFolder.objects.filter(id=folder_id)[0].folder_name
    else:
        movies = Title.objects.filter(folder__user=user).order_by('title')
        name = 'All Folders'
    context["movies"] = movies
    folders = ScrapeFolder.objects.filter(user=user)
    context["folders"] = folders
    context["num_movies"] = movies.count()

    context["page_title"] = 'Movies from: %s' % name
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

def get_cleaned_title_name(name):
    """
    Takes in a dirty title name (like with periods, release groups,etc)
    cleans it and returns that cleaned string
    """
    # TODO: Implement me.
    return name

def parse_folder(name, data, user):
    settings = ScrapeSettings.objects.all()[0]
    folder = ScrapeFolder.objects.get_or_create(name=name, user=user, location=data["path"], settings=settings)
    folder.save()
    for title in data["names"]:
        cleaned_title = get_cleaned_title_name(title)
        #try get cached title by this name then link to unique title for this user
        cached = CachedTitle.objects.get_or_create(title=cleaned_title)
        cached.save()
        user_title = Title.objects.get_or_create(cached_title=cached, folder=folder)
        user_title.save()


@login_required
def submit_data(request):
    """
        Expects a posted JSON string containing data about folders that were scraped,
            their paths and their contents.

        Login credentials are required to post, so that info is encoded in the request object.

        We take this data and update the db.

            { folder_name1: { path: '/foo/bar/folder_name1',
                              names: ['How.I.Met.Your.Mother.S01E03',
                                       'Fight.Club.xvid-medics.bdrip',
                                       'How To Catch A Predator.avi']
                            },
              folder_two: {...}
            }


        Since updating/pulling info from IMDB can take quite some time
        we don't do that immediately.  Instead we rely on a scheduled
        task to run through the database and update things periodically
        as new CachedTitle objects are created.

    """
    user = request.user
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])

    raw_data = request.POST["info"]

    json_data = json.loads(raw_data)

    if len(json_data) <= 0:
        return HttpResponseNotModified()

    for folder in json_data:
        parse_folder(folder, json_data[folder], user)

    return HttpResponse("Succesfully parsed folder information for user:%s!\n" % user)