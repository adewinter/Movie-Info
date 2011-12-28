# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Movie.rating'
        db.alter_column('imdb_movie', 'rating', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=3, decimal_places=2))

        # Changing field 'Movie.year'
        db.alter_column('imdb_movie', 'year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True))


    def backwards(self, orm):
        
        # Changing field 'Movie.rating'
        db.alter_column('imdb_movie', 'rating', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True))

        # Changing field 'Movie.year'
        db.alter_column('imdb_movie', 'year', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=10, decimal_places=2))


    models = {
        'imdb.movie': {
            'Meta': {'object_name': 'Movie'},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'folder_url': ('django.db.models.fields.CharField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'imdb_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'imdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '3', 'decimal_places': '2', 'blank': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'year': ('django.db.models.fields.IntegerField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
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
