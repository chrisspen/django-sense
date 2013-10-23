# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from sense.models import Sense

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Remember to use orm['appname.ModelName'] rather than "from appname.models..."
#        q = Sense.objects.all()
#        i = 0
#        total = q.count()
#        for s in q:
#            i += 1
#            if not i % 100:
#                print '%i of %i' % (i, total)
#            s.save()
        pass

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        'sense.example': {
            'Meta': {'object_name': 'Example'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'sense.sense': {
            'Meta': {'ordering': "('source', 'pos', 'word', 'index', 'definition')", 'unique_together': "(('source', 'word', 'pos', 'index'),)", 'object_name': 'Sense'},
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['sense.Example']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senses'", 'to': "orm['sense.Source']"}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senses'", 'to': "orm['sense.Word']"})
        },
        'sense.source': {
            'Meta': {'object_name': 'Source'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        'sense.word': {
            'Meta': {'ordering': "('text',)", 'object_name': 'Word'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['sense']
    symmetrical = True
