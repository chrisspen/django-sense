# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Context.allow_inference'
        db.add_column(u'sense_context', 'allow_inference',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Context.allow_inference'
        db.delete_column(u'sense_context', 'allow_inference')


    models = {
        u'sense.context': {
            'Meta': {'unique_together': "(('name', 'parent'),)", 'object_name': 'Context'},
            '_inferred_triple_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'inferred_triple_count'", 'blank': 'True'}),
            '_subject_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'subject_count'", 'blank': 'True'}),
            '_triple_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'triple_count'", 'blank': 'True'}),
            'allow_inference': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_inference_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'minimum_inference_weight': ('django.db.models.fields.FloatField', [], {'default': '0.01'}),
            'missing_truth_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '200'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sense.Context']"}),
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contexts'", 'symmetrical': 'False', 'to': u"orm['sense.InferenceRule']"}),
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
        u'sense.inferencerule': {
            'Meta': {'object_name': 'InferenceRule'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
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
            'inference_arguments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'inference_arguments_rel_+'", 'null': 'True', 'to': u"orm['sense.Triple']"}),
            'inference_rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sense.InferenceRule']", 'null': 'True', 'blank': 'True'}),
            'inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'inferred_weight': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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