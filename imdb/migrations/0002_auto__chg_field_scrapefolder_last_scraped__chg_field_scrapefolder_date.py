# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'ScrapeFolder.last_scraped'
        db.alter_column('imdb_scrapefolder', 'last_scraped', self.gf('django.db.models.fields.DateTimeField')(null=True))

        # Changing field 'ScrapeFolder.date_created'
        db.alter_column('imdb_scrapefolder', 'date_created', self.gf('django.db.models.fields.DateTimeField')(auto_now=True))


    def backwards(self, orm):
        
        # Changing field 'ScrapeFolder.last_scraped'
        db.alter_column('imdb_scrapefolder', 'last_scraped', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2011, 12, 26)))

        # Changing field 'ScrapeFolder.date_created'
        db.alter_column('imdb_scrapefolder', 'date_created', self.gf('django.db.models.fields.DateTimeField')())


    models = {
        'imdb.movie': {
            'Meta': {'object_name': 'Movie'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imbdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4'})
        },
        'imdb.namewordsblacklist': {
            'Meta': {'object_name': 'NameWordsBlackList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_regex': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'match_string': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'imdb.scrapefolder': {
            'Meta': {'object_name': 'ScrapeFolder'},
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'folder_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scraped': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'settings': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['imdb.ScrapeSettings']"})
        },
        'imdb.scrapesettings': {
            'Meta': {'object_name': 'ScrapeSettings'},
            'api_url': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_frequency': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['imdb']
