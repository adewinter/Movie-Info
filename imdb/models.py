from django.db import models

# Create your models here.
class Movie(models.Model):
    """
    """
    title = models.CharField(max_length=300)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    year = models.IntegerField(max_length=4,blank=True, null=True)
    imdb_url = models.URLField(blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    last_updated = models.DateTimeField(blank=True, null=True)
    imdb_title = models.CharField(max_length=255, blank=True, null=True)
    actors = models.CharField(max_length=255, blank=True, null=True)
    folder_url = models.CharField(max_length=350, blank=True, null=True)

    def __unicode__(self):
        return "Movie: %s, Rating: %s/10" % (self.title, self.rating)

class ScrapeSettings(models.Model):
    api_url = models.URLField(help_text="API URL")
    update_frequency = models.IntegerField(help_text="Minutes between checking for updates")

class ScrapeFolder(models.Model):
    folder_name = models.CharField(max_length=255)
    folder_location = models.CharField(help_text="Path to Folder", max_length=255)
    last_scraped = models.DateTimeField(null=True,blank=True)
    date_created = models.DateTimeField(auto_created=True,auto_now=True)
    settings = models.ForeignKey(ScrapeSettings)

    def __unicode__(self):
        return "Scrape Folder: %s. Last Scraped on: %s" % (self.folder_name, self.last_scraped)

class NameWordsBlackList(models.Model):
    """
        Words that should be filtered out of names
    """
    is_regex = models.BooleanField(default=False, help_text="Regex not implemented so don't check this!")
    match_string = models.CharField(max_length=200, help_text="Words in a movie name that should be filtered out")
    