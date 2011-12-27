from datetime import datetime
from decimal import Decimal
from urllib import urlencode
from urllib2 import urlopen
from django.core.management.base import BaseCommand, CommandError
import json

from imdb.models import ScrapeFolder, NameWordsBlackList, Movie, ScrapeSettings
import os


class Command(BaseCommand):
    help = "Refreshes the DB and pulls data from IMDB"

    def handle(self, *args, **options):
        folders = ScrapeFolder.objects.all()
        titles = []
        paths = []
        self.stdout.write('Getting Folders...\n')
        for folder in folders:
            self.stdout.write('Found folder: %s\n' % folder.folder_location)
            path = folder.folder_location
            titles += os.listdir(path)
            for title in titles:
                paths.append('%s' % os.path.join(path,title))

        for bad_title in titles:
            good_title = self.remove_crap(bad_title)

            movie, created = Movie.objects.get_or_create(title=good_title)
            if created or movie.rating is None:
                movie.folder_url = paths[titles.index(bad_title)]
                self.stdout.write('Cleaning up title %s => %s, path: %s \n' % (bad_title, good_title, movie.folder_url))

                self.populate_movie(movie)


        self.stdout.write('Checking for dead/deleted movies...\n')
        movies = Movie.objects.all()
        for movie in movies:
            if movie.folder_url and not os.path.exists(movie.folder_url):
                self.stdout.write('Deleting info from DB for: %s' % movie.title)
                movie.delete()

        self.stdout.write('Done!')


    def remove_crap(self, words):
        """
            Takes in a list of words and removes crappy ones (contained in the blacklist)
        """
        blacklist = [
            "dvd",
            "imdb",
            "BD.rip",
            " rip ",
            "dvdrip",
            "C100",
            "hdtv",
            "bluray",
            "bdflix",
            "mkv",
            "DTS",
            " hd ",
            " wiki ",
            " DTS ",
            "1080p",
            "720p",
            "1080",
            "720",
            "SAINAASH",
            "x264",
            "5.1",
            "HDDVD",
            "-Septic",
            "-esir",
            "Newshost",
            "-rx-",
            "brrip",

            "( )",
            "[ ]",
        ]
        more_blacklist_words = NameWordsBlackList.objects.all()

        for bword in more_blacklist_words:
            if not bword.is_regex:
                blacklist.append(bword.match_string)

        #Fianlly, append '.' and other punctuation last
        blacklist.append('.')
        blacklist.append('-')
        blacklist.append('_')
        #lowercase blacklist
        blacklist = map(lambda x: x.lower(), blacklist)
        w = words.lower()

        for bword in blacklist:
            w = w.replace(bword, ' ')

        w = ' '.join(w.split()).title().strip()
        return w


    def populate_movie(self, movie):
        if not movie.imdb_url:
            self.stdout.write('Populating Movie...%s\n' % movie.title)
            json_info = self.get_imdb_json(movie.title)
            if not json_info:
                self.stdout.write('No JSON Response returned from API\n')
                return None

            if json_info.__contains__("Plot"):
                movie.summary = json_info["Plot"]

            if json_info.__contains__("ID"):
                movie.imdb_url = "http://www.imdb.com/title/%s" % json_info["ID"]

            if json_info.__contains__("Rating") and json_info["Rating"] != "N/A":
                movie.rating = Decimal(json_info["Rating"])

            if json_info.__contains__("Year"):
                movie.year = json_info["Year"]

            if json_info.__contains__("Poster"):
                movie.image_url = json_info["Poster"]

            if json_info.__contains__("Title"):
                movie.imdb_title = json_info["Title"]

            if json_info.__contains__("Actors"):
                movie.actors = json_info["Actors"]

            movie.last_updated = datetime.now()
            movie.save()

    def get_imdb_json(self, title):
        args = urlencode({"t": title})

        api_url = ScrapeSettings.objects.all()[0].api_url
        call_url = api_url + "?" + args
        self.stdout.write("Calling %s\n" % call_url)
        result = urlopen(call_url)
        lines = result.readlines()
        if len(lines) == 0:
            return None
        result = json.loads(lines[0])
        self.stdout.write("Results:\n %s\n" % result)
        if result.__contains__("Response") and result["Response"] == "True" :
            self.stdout.write("Succesfully got a reponse from IMDBAPI for %s\n" % title)
            return result
        else:
            return None
