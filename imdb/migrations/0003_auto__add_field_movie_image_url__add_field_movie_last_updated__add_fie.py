# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Movie.image_url'
        db.add_column('imdb_movie', 'image_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True, blank=True), keep_default=False)

        # Adding field 'Movie.last_updated'
        db.add_column('imdb_movie', 'last_updated', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True), keep_default=False)

        # Adding field 'Movie.imdb_title'
        db.add_column('imdb_movie', 'imdb_title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Movie.actors'
        db.add_column('imdb_movie', 'actors', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Changing field 'Movie.imbdb_url'
        db.alter_column('imdb_movie', 'imbdb_url', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))

        # Changing field 'Movie.summary'
        db.alter_column('imdb_movie', 'summary', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Movie.year'
        db.alter_column('imdb_movie', 'year', self.gf('django.db.models.fields.IntegerField')(max_length=4, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Movie.image_url'
        db.delete_column('imdb_movie', 'image_url')

        # Deleting field 'Movie.last_updated'
        db.delete_column('imdb_movie', 'last_updated')

        # Deleting field 'Movie.imdb_title'
        db.delete_column('imdb_movie', 'imdb_title')

        # Deleting field 'Movie.actors'
        db.delete_column('imdb_movie', 'actors')

        # Changing field 'Movie.imbdb_url'
        db.alter_column('imdb_movie', 'imbdb_url', self.gf('django.db.models.fields.URLField')(default=datetime.date(2011, 12, 27), max_length=200))

        # Changing field 'Movie.summary'
        db.alter_column('imdb_movie', 'summary', self.gf('django.db.models.fields.TextField')(default=datetime.date(2011, 12, 27)))

        # Changing field 'Movie.year'
        db.alter_column('imdb_movie', 'year', self.gf('django.db.models.fields.IntegerField')(default=datetime.date(2011, 12, 27), max_length=4))


    models = {
        'imdb.movie': {
            'Meta': {'object_name': 'Movie'},
            'actors': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'imbdb_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'imdb_title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'last_updated': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'max_length': '2', 'null': 'True', 'blank': 'True'}),
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
