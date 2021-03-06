import logging
import os
import urllib
from django.contrib.auth.models import User
from django.core.files.base import File
from django.db import models
import urlparse

logging.getLogger(__name__)

class ScrapeSettings(models.Model):
    api_url = models.URLField(help_text="API URL")
    update_frequency = models.IntegerField(help_text="Minutes between checking for updates")

class ScrapeFolder(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(help_text="Path to Folder", max_length=255)
    last_scraped = models.DateTimeField(null=True,blank=True)
    date_created = models.DateTimeField(auto_created=True,auto_now=True)
    settings = models.ForeignKey(ScrapeSettings)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return "Scrape Folder: %s. Last Scraped on: %s" % (self.folder_name, self.last_scraped)


class CachedTitle(models.Model):
    """
    """
    title = models.CharField(max_length=300)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    year = models.IntegerField(max_length=4,blank=True, null=True)
    imdb_url = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    image = models.ImageField(upload_to="movies/", blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    imdb_title = models.CharField(max_length=255, blank=True, null=True)
    actors = models.CharField(max_length=255, blank=True, null=True)


    def __unicode__(self):
        return "Movie: %s, Rating: %s/10" % (self.title, self.rating)

    def cache(self):
        """Store image locally if we have a URL"""
        if self.image or not self.image_url or self.image_url.lower() == 'n/a':
            return
        
        logging.info("Caching Image for Movie: %s... URL: %s" % (self.title, self.image_url))
        result, headers = urllib.urlretrieve(self.image_url)
        logging.debug('HEADERS: %s' % headers)
        logging.info("Successfully downloaded image for %s" % self.title)
        f = File(open(result, 'rb')) #ensure opening as binary!
        image_name = os.path.basename(self.image_url)
        self.image.save(image_name, f)
        logging.info("Saved Image for Movie: %s" % self.title)
        self.save()



class Title(models.Model):
    """
    A Movie/Series title associated with a specific user.  Points to a CachedTitle
    for actual IMDB data.
    """

    cached_title = models.ForeignKey(CachedTitle, related_name='user_titles')
    folder = models.ForeignKey(ScrapeFolder, null=True, blank=True)

    
class NameWordsBlackList(models.Model):
    """
        Words that should be filtered out of names
    """
    is_regex = models.BooleanField(default=False, help_text="Regex not implemented so don't check this!")
    match_string = models.CharField(max_length=200, help_text="Words in a movie name that should be filtered out REMEMBER TITLE IS CONVERTED TO LOWERCASE")
    parse_order = models.IntegerField(max_length=4, default=9999, help_text="The order in which this blacklist word should be stripped relateive to other blacklist words")
    replace_char = models.CharField(max_length=10, help_text="The character to replace the match string with. Default is blank space (' ')", default=' ')

    def __unicode__(self):
        return "Word to Strip: %s :: Order: %s" % (self.match_string, self.parse_order)