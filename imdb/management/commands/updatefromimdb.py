from django.core.management.base import BaseCommand, CommandError

from imdb.models import ScrapeFolder, NameWordsBlackList, Movie
import os


class Command(BaseCommand):
    help = "Refreshes the DB and pulls data from IMDB"

    def handle(self, *args, **options):
        folders = ScrapeFolder.objects.all()
        titles = []
        for folder in folders:
            path = folder.folder_location
            titles += os.listdir(path)

        for bad_title in titles:
            good_title = self.remove_crap(bad_title)
            self.stdout.write('%s \n' % (good_title))
            movie, created = Movie.objects.get_or_create(title=good_title)
            if created or movie.rating is None:
                self.populate_movie(movie)


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


    def populate_movie(self):
        pass