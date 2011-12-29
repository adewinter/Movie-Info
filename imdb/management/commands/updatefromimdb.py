from datetime import datetime
from decimal import Decimal
from urllib import urlencode
from urllib2 import urlopen
from django.core.management.base import BaseCommand
import json
import logging
from imdb.models import ScrapeFolder, NameWordsBlackList, Movie, ScrapeSettings
import os

logging.getLogger(__name__)

class Command(BaseCommand):
    help = "Refreshes the DB and pulls data from IMDB"

    def handle(self, *args, **options):
        folders = ScrapeFolder.objects.all()
        titles = []
        paths = []
        self.stdout.write('Getting Folders...\n')
        logging.debug('Getting Folders...')
        for folder in folders:
            self.stdout.write('Found folder: %s\n' % folder.folder_location)
            logging.debug('Found folder: %s' % folder.folder_location)
            path = folder.folder_location
            for title in os.listdir(path):
                titles.append((title, os.path.join(path,title), folder))

        for title in titles:
            bad_title = title[0]
            location = title[1]
            good_title = self.remove_crap(bad_title)
            folder = title[2]
            movie, created = Movie.objects.get_or_create(title=good_title)
            if created or movie.rating is None:
                movie.folder_url = location
                movie.folder = folder
                self.stdout.write('Cleaning up title %s => %s, path: %s \n' % (bad_title, good_title, movie.folder_url))
                logging.debug('Cleaning up title %s => %s, path: %s ' % (bad_title, good_title, movie.folder_url))
                self.populate_movie(movie)
                ##Cache the thumbnail image locally
                movie.cache()
                movie.save()


        self.stdout.write('Checking for dead/deleted movies...\n')
        logging.debug('Checking for dead/deleted movies...')
        movies = Movie.objects.all()
        for movie in movies:
            if movie.folder_url and not os.path.exists(movie.folder_url):
                self.stdout.write('Deleting info from DB for: %s' % movie.title)
                logging.debug('Deleting info from DB for: %s' % movie.title)
                movie.delete()

        self.stdout.write('Done!')
        logging.debug('Done!')


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
            logging.debug('Populating Movie...%s' % movie.title)
            json_info = self.get_imdb_json(movie.title)
            if not json_info:
                self.stdout.write('No JSON Response returned from API\n')
                logging.debug('No JSON Response returned from API')
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
        logging.debug("Calling %s" % call_url)
        result = urlopen(call_url)
        lines = result.readlines()
        if len(lines) is 0:
            return None
        result = json.loads(lines[0])
        self.stdout.write("Results:\n %s\n" % result)
        logging.debug("Results:\n %s" % result)
        if result.__contains__("Response") and result["Response"] == "True" :
            self.stdout.write("Succesfully got a reponse from IMDBAPI for %s\n" % title)
            logging.debug("Succesfully got a reponse from IMDBAPI for %s" % title)
            return result
        else:
            return None
