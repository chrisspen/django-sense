# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'subject_split']
        db.delete_unique(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'subject_split_id'])

        # Removing unique constraint on 'PredicateObjectIndexToSelf', fields ['lower', 'upper']
        db.delete_unique(u'sense_predicateobjectindextoself', ['lower_id', 'upper_id'])

        # Deleting model 'PredicateObjectIndexToSelf'
        db.delete_table(u'sense_predicateobjectindextoself')

        # Deleting field 'PredicateObjectIndex.subject_split'
        db.delete_column(u'sense_predicateobjectindex', 'subject_split_id')

        # Adding field 'PredicateObjectIndex.subject'
        db.add_column(u'sense_predicateobjectindex', 'subject',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='subject_index', null=True, to=orm['sense.Sense']),
                      keep_default=False)

        # Adding field 'PredicateObjectIndex.best_splitter'
        db.add_column(u'sense_predicateobjectindex', 'best_splitter',
                      self.gf('django.db.models.fields.NullBooleanField')(db_index=True, null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'PredicateObjectIndex', fields ['context', 'subject', 'best_splitter', 'depth']
        db.create_unique(u'sense_predicateobjectindex', ['context_id', 'subject_id', 'best_splitter', 'depth'])

        # Adding unique constraint on 'PredicateObjectIndex', fields ['context', 'subject', 'parent', 'predicate', 'object']
        db.create_unique(u'sense_predicateobjectindex', ['context_id', 'subject_id', 'parent_id', 'predicate_id', 'object_id'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'subject_split']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'subject_split_id'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'subject_split']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'subject_split_id'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'subject']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'subject_id'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'subject']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'subject_id'])


    def backwards(self, orm):
        # Removing index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'subject']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'subject_id'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'subject']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'subject_id'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'subject_split']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'subject_split_id'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'subject_split']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'subject_split_id'])

        # Removing unique constraint on 'PredicateObjectIndex', fields ['context', 'subject', 'parent', 'predicate', 'object']
        db.delete_unique(u'sense_predicateobjectindex', ['context_id', 'subject_id', 'parent_id', 'predicate_id', 'object_id'])

        # Removing unique constraint on 'PredicateObjectIndex', fields ['context', 'subject', 'best_splitter', 'depth']
        db.delete_unique(u'sense_predicateobjectindex', ['context_id', 'subject_id', 'best_splitter', 'depth'])

        # Adding model 'PredicateObjectIndexToSelf'
        db.create_table(u'sense_predicateobjectindextoself', (
            ('upper', self.gf('django.db.models.fields.related.ForeignKey')(related_name='upper_poi_m2m', to=orm['sense.PredicateObjectIndex'])),
            ('lower', self.gf('django.db.models.fields.related.ForeignKey')(related_name='lower_poi_m2m', to=orm['sense.PredicateObjectIndex'])),
            ('entropy', self.gf('django.db.models.fields.FloatField')(blank=True, null=True, db_index=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, blank=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(blank=True, null=True, db_index=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'sense', ['PredicateObjectIndexToSelf'])

        # Adding unique constraint on 'PredicateObjectIndexToSelf', fields ['lower', 'upper']
        db.create_unique(u'sense_predicateobjectindextoself', ['lower_id', 'upper_id'])

        # Adding field 'PredicateObjectIndex.subject_split'
        db.add_column(u'sense_predicateobjectindex', 'subject_split',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='subject_index', null=True, to=orm['sense.Sense'], blank=True),
                      keep_default=False)

        # Deleting field 'PredicateObjectIndex.subject'
        db.delete_column(u'sense_predicateobjectindex', 'subject_id')

        # Deleting field 'PredicateObjectIndex.best_splitter'
        db.delete_column(u'sense_predicateobjectindex', 'best_splitter')

        # Adding unique constraint on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'subject_split']
        db.create_unique(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'subject_split_id'])


    models = {
        u'sense.context': {
            'Meta': {'unique_together': "(('name', 'parent'),)", 'object_name': 'Context'},
            '_subject_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'subject_count'", 'blank': 'True'}),
            '_triple_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'triple_count'", 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'missing_truth_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sense.Context']"}),
            'top_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'top_children'", 'null': 'True', 'to': u"orm['sense.Context']"}),
            'triples': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contexts'", 'symmetrical': 'False', 'to': u"orm['sense.Triple']"}),
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
        u'sense.predicateobjectindex': {
            'Meta': {'ordering': "('-entropy',)", 'unique_together': "(('context', 'subject', 'parent', 'predicate', 'object'), ('context', 'subject', 'best_splitter', 'depth'))", 'object_name': 'PredicateObjectIndex', 'index_together': "(('context', 'parent', 'predicate', 'object', 'subject'), ('context', 'predicate', 'object', 'subject'), ('context', 'parent', 'predicate', 'object'), ('context', 'predicate', 'object'))"},
            '_triple_ids': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'triple_ids'", 'blank': 'True'}),
            'best_splitter': ('django.db.models.fields.NullBooleanField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'context': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_object_indexes'", 'to': u"orm['sense.Context']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'entropy': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'fresh': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'object_index'", 'to': u"orm['sense.Sense']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sense.PredicateObjectIndex']", 'null': 'True', 'blank': 'True'}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_index'", 'to': u"orm['sense.Sense']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subject_index'", 'null': 'True', 'to': u"orm['sense.Sense']"}),
            'subject_count_direct': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'subject_count_total': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'sense.predicateobjectindexpending': {
            'Meta': {'object_name': 'PredicateObjectIndexPending', 'managed': 'False'},
            'context': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sense.Context']", 'on_delete': 'models.DO_NOTHING', 'db_column': "'context_id'"}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'object_index_pending'", 'on_delete': 'models.DO_NOTHING', 'db_column': "'object_id'", 'to': u"orm['sense.Sense']"}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_index_pending'", 'on_delete': 'models.DO_NOTHING', 'db_column': "'predicate_id'", 'to': u"orm['sense.Sense']"}),
            'subject_count_direct': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'sense.sense': {
            'Meta': {'ordering': "('source', 'pos', 'word', 'definition')", 'unique_together': "(('source', 'word', 'pos', 'definition'), ('source', 'word', 'pos', 'wordnet_id'))", 'object_name': 'Sense'},
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'allow_predicate_usage': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'conceptnet_predicate': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'conceptnet_uri': ('django.db.models.fields.URLField', [], {'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'definition': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'examples': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sense.Example']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2'}),
            'mutually_exclusive_subject_predicate': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pos': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '5', 'db_index': 'True'}),
            'reverse_transitive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'senses'", 'null': 'True', 'to': u"orm['sense.Source']"}),
            'transitive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'word': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'senses'", 'to': u"orm['sense.Word']"}),
            'wordnet_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'})
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
            'Meta': {'unique_together': "(('subject', 'predicate', 'object'),)", 'object_name': 'Triple', 'index_together': "(('predicate', 'object'),)"},
            'conceptnet_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'conceptnet_surface_text': ('django.db.models.fields.CharField', [], {'max_length': '7700', 'null': 'True', 'blank': 'True'}),
            'conceptnet_uri': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'conceptnet_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'log_prob': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'object_triples'", 'null': 'True', 'to': u"orm['sense.Sense']"}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_triples'", 'to': u"orm['sense.Sense']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subject_triples'", 'to': u"orm['sense.Sense']"}),
            'subject_inferences_fresh': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'total_contexts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'weight_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'weight_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'sense.word': {
            'Meta': {'ordering': "('text',)", 'object_name': 'Word'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sense_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '700', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'wiktionary_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sense']