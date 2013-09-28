# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'index']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'index'])

        # Adding model 'Context'
        db.create_table(u'sense_context', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='global', max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sense.Context'], null=True, blank=True)),
        ))
        db.send_create_signal(u'sense', ['Context'])

        # Adding unique constraint on 'Context', fields ['name', 'parent']
        db.create_unique(u'sense_context', ['name', 'parent_id'])

        # Adding model 'Triple'
        db.create_table(u'sense_triple', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('context', self.gf('django.db.models.fields.related.ForeignKey')(related_name='triples', to=orm['sense.Context'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subject_triples', to=orm['sense.Sense'])),
            ('predicate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='predicate_triples', to=orm['sense.Sense'])),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='object_triples', null=True, to=orm['sense.Sense'])),
            ('weight_sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('weight_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'sense', ['Triple'])

        # Adding unique constraint on 'Triple', fields ['context', 'subject', 'predicate', 'object']
        db.create_unique(u'sense_triple', ['context_id', 'subject_id', 'predicate_id', 'object_id'])

        # Deleting field 'Sense.index'
        db.delete_column(u'sense_sense', 'index')

        # Adding field 'Sense.created'
        db.add_column(u'sense_sense', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'Sense.updated'
        db.add_column(u'sense_sense', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'Sense.deleted'
        db.add_column(u'sense_sense', 'deleted',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Sense.wordnet_id'
        db.add_column(u'sense_sense', 'wordnet_id',
                      self.gf('django.db.models.fields.CharField')(db_index=True, max_length=700, unique=True, null=True, blank=True),
                      keep_default=False)

        # Adding index on 'Sense', fields ['pos']
        db.create_index(u'sense_sense', ['pos'])

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition'])

        # Adding field 'Word.created'
        db.add_column(u'sense_word', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'Word.updated'
        db.add_column(u'sense_word', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'Word.deleted'
        db.add_column(u'sense_word', 'deleted',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Word.text'
        db.alter_column(u'sense_word', 'text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=700))
        # Adding index on 'Word', fields ['text']
        db.create_index(u'sense_word', ['text'])

        # Adding field 'Source.created'
        db.add_column(u'sense_source', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'Source.updated'
        db.add_column(u'sense_source', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'Source.deleted'
        db.add_column(u'sense_source', 'deleted',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True),
                      keep_default=False)

        # Adding index on 'Source', fields ['name']
        db.create_index(u'sense_source', ['name'])

        # Adding field 'Example.created'
        db.add_column(u'sense_example', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'Example.updated'
        db.add_column(u'sense_example', 'updated',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True),
                      keep_default=False)

        # Adding field 'Example.deleted'
        db.add_column(u'sense_example', 'deleted',
                      self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Removing index on 'Source', fields ['name']
        db.delete_index(u'sense_source', ['name'])

        # Removing index on 'Word', fields ['text']
        db.delete_index(u'sense_word', ['text'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition'])

        # Removing index on 'Sense', fields ['pos']
        db.delete_index(u'sense_sense', ['pos'])

        # Removing unique constraint on 'Triple', fields ['context', 'subject', 'predicate', 'object']
        db.delete_unique(u'sense_triple', ['context_id', 'subject_id', 'predicate_id', 'object_id'])

        # Removing unique constraint on 'Context', fields ['name', 'parent']
        db.delete_unique(u'sense_context', ['name', 'parent_id'])

        # Deleting model 'Context'
        db.delete_table(u'sense_context')

        # Deleting model 'Triple'
        db.delete_table(u'sense_triple')

        # Adding field 'Sense.index'
        db.add_column(u'sense_sense', 'index',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=1),
                      keep_default=False)

        # Deleting field 'Sense.created'
        db.delete_column(u'sense_sense', 'created')

        # Deleting field 'Sense.updated'
        db.delete_column(u'sense_sense', 'updated')

        # Deleting field 'Sense.deleted'
        db.delete_column(u'sense_sense', 'deleted')

        # Deleting field 'Sense.wordnet_id'
        db.delete_column(u'sense_sense', 'wordnet_id')

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'index']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'index'])

        # Deleting field 'Word.created'
        db.delete_column(u'sense_word', 'created')

        # Deleting field 'Word.updated'
        db.delete_column(u'sense_word', 'updated')

        # Deleting field 'Word.deleted'
        db.delete_column(u'sense_word', 'deleted')


        # Changing field 'Word.text'
        db.alter_column(u'sense_word', 'text', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True))
        # Deleting field 'Source.created'
        db.delete_column(u'sense_source', 'created')

        # Deleting field 'Source.updated'
        db.delete_column(u'sense_source', 'updated')

        # Deleting field 'Source.deleted'
        db.delete_column(u'sense_source', 'deleted')

        # Deleting field 'Example.created'
        db.delete_column(u'sense_example', 'created')

        # Deleting field 'Example.updated'
        db.delete_column(u'sense_example', 'updated')

        # Deleting field 'Example.deleted'
        db.delete_column(u'sense_example', 'deleted')


    models = {
        u'sense.context': {
            'Meta': {'unique_together': "(('name', 'parent'),)", 'object_name': 'Context'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sense.Context']", 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'sense.example': {
            'Meta': {'object_name': 'Example'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'sense.sense': {
            'Meta': {'ordering': "('source', 'pos', 'word', 'definition')", 'unique_together': "(('source', 'word', 'pos', 'definition'),)", 'object_name': 'Sense'},
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sense.Example']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'max_length': '5', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senses'", 'to': u"orm['sense.Source']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senses'", 'to': u"orm['sense.Word']"}),
            'wordnet_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'unique': 'True', 'null': 'True', 'blank': 'True'})
        },
        u'sense.source': {
            'Meta': {'object_name': 'Source'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'sense.triple': {
            'Meta': {'unique_together': "(('context', 'subject', 'predicate', 'object'),)", 'object_name': 'Triple'},
            'context': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'triples'", 'to': u"orm['sense.Context']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'object_triples'", 'null': 'True', 'to': u"orm['sense.Sense']"}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_triples'", 'to': u"orm['sense.Sense']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject_triples'", 'to': u"orm['sense.Sense']"}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'weight_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'weight_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'sense.word': {
            'Meta': {'ordering': "('text',)", 'object_name': 'Word'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '700', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        }
    }

    complete_apps = ['sense']