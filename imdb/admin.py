from django.contrib import admin
from imdb.models import Title, CachedTitle, NameWordsBlackList,ScrapeFolder,ScrapeSettings

admin.site.register(Title)
admin.site.register(CachedTitle)
admin.site.register(NameWordsBlackList)
admin.site.register(ScrapeFolder)
admin.site.register(ScrapeSettings)
