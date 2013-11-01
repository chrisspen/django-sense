# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Triple', fields ['subject', 'subject_triple', 'predicate', 'object', 'object_triple']
        db.delete_unique(u'sense_triple', ['subject_id', 'subject_triple_id', 'predicate_id', 'object_id', 'object_triple_id'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'wordnet_id']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'wordnet_id'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition'])

        # Adding field 'Sense.owner'
        db.add_column(u'sense_sense', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition', 'owner']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition', 'owner_id'])

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'wordnet_id', 'owner']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'wordnet_id', 'owner_id'])

        # Adding field 'Triple.owner'
        db.add_column(u'sense_triple', 'owner',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True),
                      keep_default=False)

        # Adding unique constraint on 'Triple', fields ['subject', 'subject_triple', 'predicate', 'object', 'object_triple', 'owner']
        db.create_unique(u'sense_triple', ['subject_id', 'subject_triple_id', 'predicate_id', 'object_id', 'object_triple_id', 'owner_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Triple', fields ['subject', 'subject_triple', 'predicate', 'object', 'object_triple', 'owner']
        db.delete_unique(u'sense_triple', ['subject_id', 'subject_triple_id', 'predicate_id', 'object_id', 'object_triple_id', 'owner_id'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'wordnet_id', 'owner']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'wordnet_id', 'owner_id'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition', 'owner']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition', 'owner_id'])

        # Deleting field 'Sense.owner'
        db.delete_column(u'sense_sense', 'owner_id')

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition'])

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'wordnet_id']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'wordnet_id'])

        # Deleting field 'Triple.owner'
        db.delete_column(u'sense_triple', 'owner_id')

        # Adding unique constraint on 'Triple', fields ['subject', 'subject_triple', 'predicate', 'object', 'object_triple']
        db.create_unique(u'sense_triple', ['subject_id', 'subject_triple_id', 'predicate_id', 'object_id', 'object_triple_id'])


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'sense.context': {
            'Meta': {'unique_together': "(('name', 'parent', 'owner'),)", 'object_name': 'Context'},
            '_inferred_triple_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'inferred_triple_count'", 'blank': 'True'}),
            '_subject_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'subject_count'", 'blank': 'True'}),
            '_triple_count': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'db_column': "'triple_count'", 'blank': 'True'}),
            'accessibility': ('django.db.models.fields.CharField', [], {'default': "'private'", 'max_length': '25', 'db_index': 'True'}),
            'all_senses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'all_senses_contexts'", 'symmetrical': 'False', 'to': u"orm['sense.Sense']"}),
            'all_triples': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'all_triples_contexts'", 'symmetrical': 'False', 'to': u"orm['sense.Triple']"}),
            'allow_inference': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'editability': ('django.db.models.fields.CharField', [], {'default': "'owner-only'", 'max_length': '25', 'db_index': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'fresh_all_triples': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'maximum_inference_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '20'}),
            'minimum_inference_weight': ('django.db.models.fields.FloatField', [], {'default': '0.01'}),
            'missing_truth_value': ('django.db.models.fields.FloatField', [], {'default': '0.0'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "'global'", 'max_length': '200'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sense.Context']"}),
            'rules': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contexts'", 'symmetrical': 'False', 'to': u"orm['sense.InferenceRule']"}),
            'senses': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'senses_contexts'", 'symmetrical': 'False', 'to': u"orm['sense.Sense']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '500', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'top_parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'top_children'", 'null': 'True', 'to': u"orm['sense.Context']"}),
            'triples': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'direct_contexts'", 'symmetrical': 'False', 'to': u"orm['sense.Triple']"}),
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
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'simple_description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'transitive_predicate': ('django.db.models.fields.CharField', [], {'default': "'IsA'", 'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'sense.predicateobjectindex': {
            'Meta': {'ordering': "('-entropy',)", 'unique_together': "(('context', 'parent', 'predicate', 'object', 'prior'), ('context', 'parent', 'prior', 'best_splitter'))", 'object_name': 'PredicateObjectIndex', 'index_together': "(('context', 'parent', 'prior'), ('context', 'parent', 'predicate', 'object', 'prior'), ('context', 'predicate', 'object', 'prior'), ('context', 'parent', 'predicate', 'object', 'prior'), ('context', 'predicate', 'object', 'prior'))"},
            '_triple_ids': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'triple_ids'", 'blank': 'True'}),
            'best_splitter': ('django.db.models.fields.NullBooleanField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'check_enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'context': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_object_indexes'", 'to': u"orm['sense.Context']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'depth': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'entropy': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'fresh': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'object_index'", 'to': u"orm['sense.Sense']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['sense.PredicateObjectIndex']"}),
            'po_hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_index'", 'to': u"orm['sense.Sense']"}),
            'prior': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
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
            'Meta': {'ordering': "('word__text',)", 'unique_together': "(('source', 'word', 'pos', 'definition', 'owner'), ('source', 'word', 'pos', 'wordnet_id', 'owner'))", 'object_name': 'Sense'},
            '_name': ('django.db.models.fields.CharField', [], {'max_length': '700', 'null': 'True', 'blank': 'True'}),
            '_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'text'", 'blank': 'True'}),
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
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'pos': ('django.db.models.fields.CharField', [], {'default': "'n'", 'max_length': '5', 'db_index': 'True'}),
            'reverse_transitive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'source': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'senses'", 'null': 'True', 'to': u"orm['sense.Source']"}),
            'transitive': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'trusted': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
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
            'Meta': {'ordering': "('_text',)", 'unique_together': "(('subject', 'subject_triple', 'predicate', 'object', 'object_triple', 'owner'),)", 'object_name': 'Triple', 'index_together': "(('predicate', 'object', 'object_triple'), ('inferred', 'deleted'))"},
            '_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'db_column': "'text'", 'blank': 'True'}),
            'conceptnet_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'conceptnet_surface_text': ('django.db.models.fields.CharField', [], {'max_length': '7700', 'null': 'True', 'blank': 'True'}),
            'conceptnet_uri': ('django.db.models.fields.URLField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'conceptnet_weight': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inference_arguments': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'inference_arguments_rel_+'", 'null': 'True', 'to': u"orm['sense.Triple']"}),
            'inference_depth': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'inference_rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sense.InferenceRule']", 'null': 'True', 'blank': 'True'}),
            'inferred': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'inferred_weight': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'log_prob': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'object': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'object_triples'", 'null': 'True', 'to': u"orm['sense.Sense']"}),
            'object_triple': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'object_triple_triples'", 'null': 'True', 'to': u"orm['sense.Triple']"}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'po_hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'predicate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'predicate_triples'", 'to': u"orm['sense.Sense']"}),
            'search_index': ('djorm_pgfulltext.fields.VectorField', [], {'default': "''", 'null': 'True', 'db_index': 'True'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subject_triples'", 'null': 'True', 'to': u"orm['sense.Sense']"}),
            'subject_inferences_fresh': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'subject_triple': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'subject_triple_triples'", 'null': 'True', 'to': u"orm['sense.Triple']"}),
            'total_contexts': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'weight': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'weight_sum': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'weight_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'sense.tripleinference': {
            'Meta': {'unique_together': "(('inferred_triple', 'inference_rule', 'inference_arguments_cache'),)", 'object_name': 'TripleInference'},
            'confirmed': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inference_arguments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['sense.Triple']", 'null': 'True', 'blank': 'True'}),
            'inference_arguments_cache': ('django.db.models.fields.CharField', [], {'max_length': '700', 'null': 'True', 'blank': 'True'}),
            'inference_rule': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['sense.InferenceRule']", 'null': 'True', 'blank': 'True'}),
            'inferred_triple': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'inferences'", 'to': u"orm['sense.Triple']"}),
            'inferred_weight': ('django.db.models.fields.FloatField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'})
        },
        u'sense.word': {
            'Meta': {'ordering': "('text',)", 'object_name': 'Word'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sense_count': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'db_index': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '700', 'db_index': 'True'}),
            'trusted': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'wiktionary_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sense']