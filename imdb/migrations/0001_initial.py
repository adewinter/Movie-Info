# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Movie'
        db.create_table('imdb_movie', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('rating', self.gf('django.db.models.fields.IntegerField')(max_length=2, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(max_length=4)),
            ('imbdb_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('summary', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('imdb', ['Movie'])

        # Adding model 'ScrapeSettings'
        db.create_table('imdb_scrapesettings', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('api_url', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('update_frequency', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('imdb', ['ScrapeSettings'])

        # Adding model 'ScrapeFolder'
        db.create_table('imdb_scrapefolder', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('folder_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('folder_location', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('last_scraped', self.gf('django.db.models.fields.DateTimeField')()),
            ('date_created', self.gf('django.db.models.fields.DateTimeField')()),
            ('settings', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['imdb.ScrapeSettings'])),
        ))
        db.send_create_signal('imdb', ['ScrapeFolder'])

        # Adding model 'NameWordsBlackList'
        db.create_table('imdb_namewordsblacklist', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('is_regex', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('match_string', self.gf('django.db.models.fields.CharField')(max_length=200)),
        ))
        db.send_create_signal('imdb', ['NameWordsBlackList'])


    def backwards(self, orm):
        
        # Deleting model 'Movie'
        db.delete_table('imdb_movie')

        # Deleting model 'ScrapeSettings'
        db.delete_table('imdb_scrapesettings')

        # Deleting model 'ScrapeFolder'
        db.delete_table('imdb_scrapefolder')

        # Deleting model 'NameWordsBlackList'
        db.delete_table('imdb_namewordsblacklist')


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
            'date_created': ('django.db.models.fields.DateTimeField', [], {}),
            'folder_location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'folder_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_scraped': ('django.db.models.fields.DateTimeField', [], {}),
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
