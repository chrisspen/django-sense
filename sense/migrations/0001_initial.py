# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table('sense_source', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('sense', ['Source'])

        # Adding model 'Word'
        db.create_table('sense_word', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal('sense', ['Word'])

        # Adding model 'Example'
        db.create_table('sense_example', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sense', ['Example'])

        # Adding model 'Sense'
        db.create_table('sense_sense', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(related_name='senses', to=orm['sense.Source'])),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(related_name='senses', to=orm['sense.Word'])),
            ('pos', self.gf('django.db.models.fields.CharField')(max_length=5)),
            ('index', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('sense', ['Sense'])

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'index']
        db.create_unique('sense_sense', ['source_id', 'word_id', 'pos', 'index'])

        # Adding M2M table for field examples on 'Sense'
        db.create_table('sense_sense_examples', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sense', models.ForeignKey(orm['sense.sense'], null=False)),
            ('example', models.ForeignKey(orm['sense.example'], null=False))
        ))
        db.create_unique('sense_sense_examples', ['sense_id', 'example_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'index']
        db.delete_unique('sense_sense', ['source_id', 'word_id', 'pos', 'index'])

        # Deleting model 'Source'
        db.delete_table('sense_source')

        # Deleting model 'Word'
        db.delete_table('sense_word')

        # Deleting model 'Example'
        db.delete_table('sense_example')

        # Deleting model 'Sense'
        db.delete_table('sense_sense')

        # Removing M2M table for field examples on 'Sense'
        db.delete_table('sense_sense_examples')


    models = {
        'sense.example': {
            'Meta': {'object_name': 'Example'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {})
        },
        'sense.sense': {
            'Meta': {'ordering': "('source', 'pos', 'word', 'index', 'definition')", 'unique_together': "(('source', 'word', 'pos', 'index'),)", 'object_name': 'Sense'},
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