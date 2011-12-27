from django.contrib import admin
from imdb.models import Movie,NameWordsBlackList,ScrapeFolder,ScrapeSettings

admin.site.register(Movie)
admin.site.register(NameWordsBlackList)
admin.site.register(ScrapeFolder)
admin.site.register(ScrapeSettings)
