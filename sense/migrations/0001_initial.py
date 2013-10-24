# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Source'
        db.create_table(u'sense_source', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255, db_index=True)),
        ))
        db.send_create_signal(u'sense', ['Source'])

        # Adding model 'Word'
        db.create_table(u'sense_word', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.CharField')(unique=True, max_length=700, db_index=True)),
            ('wiktionary_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=700, null=True, blank=True)),
            ('sense_count', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('trusted', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
        ))
        db.send_create_signal(u'sense', ['Word'])

        # Adding model 'Example'
        db.create_table(u'sense_example', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('text', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'sense', ['Example'])

        # Adding model 'Sense'
        db.create_table(u'sense_sense', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='senses', null=True, to=orm['sense.Source'])),
            ('word', self.gf('django.db.models.fields.related.ForeignKey')(related_name='senses', to=orm['sense.Word'])),
            ('pos', self.gf('django.db.models.fields.CharField')(default='n', max_length=5, db_index=True)),
            ('wordnet_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=700, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='en', max_length=2)),
            ('conceptnet_uri', self.gf('django.db.models.fields.URLField')(max_length=700, null=True, blank=True)),
            ('conceptnet_predicate', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('transitive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('reverse_transitive', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('mutually_exclusive_subject_predicate', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_predicate_usage', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('definition', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('trusted', self.gf('django.db.models.fields.BooleanField')(default=True, db_index=True)),
            ('_name', self.gf('django.db.models.fields.CharField')(max_length=700, null=True, blank=True)),
        ))
        db.send_create_signal(u'sense', ['Sense'])

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition'])

        # Adding unique constraint on 'Sense', fields ['source', 'word', 'pos', 'wordnet_id']
        db.create_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'wordnet_id'])

        # Adding M2M table for field examples on 'Sense'
        m2m_table_name = db.shorten_name(u'sense_sense_examples')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('sense', models.ForeignKey(orm[u'sense.sense'], null=False)),
            ('example', models.ForeignKey(orm[u'sense.example'], null=False))
        ))
        db.create_unique(m2m_table_name, ['sense_id', 'example_id'])

        # Adding model 'InferenceRule'
        db.create_table(u'sense_inferencerule', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
            ('type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100, db_index=True)),
        ))
        db.send_create_signal(u'sense', ['InferenceRule'])

        # Adding model 'Context'
        db.create_table(u'sense_context', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(default='global', max_length=200)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['sense.Context'])),
            ('top_parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='top_children', null=True, to=orm['sense.Context'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('missing_truth_value', self.gf('django.db.models.fields.FloatField')(default=0.0)),
            ('allow_inference', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('maximum_inference_depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=20)),
            ('minimum_inference_weight', self.gf('django.db.models.fields.FloatField')(default=0.01)),
            ('_triple_count', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, db_column='triple_count', blank=True)),
            ('_inferred_triple_count', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, db_column='inferred_triple_count', blank=True)),
            ('_subject_count', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, db_column='subject_count', blank=True)),
            ('fresh_all_triples', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'sense', ['Context'])

        # Adding unique constraint on 'Context', fields ['name', 'parent', 'owner']
        db.create_unique(u'sense_context', ['name', 'parent_id', 'owner_id'])

        # Adding M2M table for field triples on 'Context'
        m2m_table_name = db.shorten_name(u'sense_context_triples')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('context', models.ForeignKey(orm[u'sense.context'], null=False)),
            ('triple', models.ForeignKey(orm[u'sense.triple'], null=False))
        ))
        db.create_unique(m2m_table_name, ['context_id', 'triple_id'])

        # Adding M2M table for field all_triples on 'Context'
        m2m_table_name = db.shorten_name(u'sense_context_all_triples')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('context', models.ForeignKey(orm[u'sense.context'], null=False)),
            ('triple', models.ForeignKey(orm[u'sense.triple'], null=False))
        ))
        db.create_unique(m2m_table_name, ['context_id', 'triple_id'])

        # Adding M2M table for field rules on 'Context'
        m2m_table_name = db.shorten_name(u'sense_context_rules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('context', models.ForeignKey(orm[u'sense.context'], null=False)),
            ('inferencerule', models.ForeignKey(orm[u'sense.inferencerule'], null=False))
        ))
        db.create_unique(m2m_table_name, ['context_id', 'inferencerule_id'])

        # Adding model 'Triple'
        db.create_table(u'sense_triple', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subject_triples', to=orm['sense.Sense'])),
            ('predicate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='predicate_triples', to=orm['sense.Sense'])),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='object_triples', null=True, to=orm['sense.Sense'])),
            ('po_hash', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=700, null=True, blank=True)),
            ('conceptnet_uri', self.gf('django.db.models.fields.URLField')(db_index=True, max_length=700, null=True, blank=True)),
            ('conceptnet_weight', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('conceptnet_surface_text', self.gf('django.db.models.fields.CharField')(max_length=7700, null=True, blank=True)),
            ('conceptnet_id', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=200, null=True, blank=True)),
            ('weight_sum', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('weight_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('weight', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('log_prob', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('total_contexts', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('inferred', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('inference_depth', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, db_index=True)),
            ('inferred_weight', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('inference_rule', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sense.InferenceRule'], null=True, blank=True)),
            ('subject_inferences_fresh', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
        ))
        db.send_create_signal(u'sense', ['Triple'])

        # Adding unique constraint on 'Triple', fields ['subject', 'predicate', 'object']
        db.create_unique(u'sense_triple', ['subject_id', 'predicate_id', 'object_id'])

        # Adding index on 'Triple', fields ['predicate', 'object']
        db.create_index(u'sense_triple', ['predicate_id', 'object_id'])

        # Adding index on 'Triple', fields ['inferred', 'deleted']
        db.create_index(u'sense_triple', ['inferred', 'deleted'])

        # Adding M2M table for field inference_arguments on 'Triple'
        m2m_table_name = db.shorten_name(u'sense_triple_inference_arguments')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_triple', models.ForeignKey(orm[u'sense.triple'], null=False)),
            ('to_triple', models.ForeignKey(orm[u'sense.triple'], null=False))
        ))
        db.create_unique(m2m_table_name, ['from_triple_id', 'to_triple_id'])

        # Adding model 'PredicateObjectIndex'
        db.create_table(u'sense_predicateobjectindex', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now_add=True, db_index=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, auto_now=True, blank=True, auto_now_add=True, null=True, db_index=True)),
            ('deleted', self.gf('django.db.models.fields.DateTimeField')(db_index=True, null=True, blank=True)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='children', null=True, to=orm['sense.PredicateObjectIndex'])),
            ('context', self.gf('django.db.models.fields.related.ForeignKey')(related_name='predicate_object_indexes', to=orm['sense.Context'])),
            ('predicate', self.gf('django.db.models.fields.related.ForeignKey')(related_name='predicate_index', to=orm['sense.Sense'])),
            ('object', self.gf('django.db.models.fields.related.ForeignKey')(related_name='object_index', to=orm['sense.Sense'])),
            ('po_hash', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=700, null=True, blank=True)),
            ('prior', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True)),
            ('depth', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('fresh', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('check_enabled', self.gf('django.db.models.fields.BooleanField')(default=False, db_index=True)),
            ('subject_count_total', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True, null=True, blank=True)),
            ('entropy', self.gf('django.db.models.fields.FloatField')(db_index=True, null=True, blank=True)),
            ('best_splitter', self.gf('django.db.models.fields.NullBooleanField')(db_index=True, null=True, blank=True)),
            ('_triple_ids', self.gf('django.db.models.fields.TextField')(null=True, db_column='triple_ids', blank=True)),
        ))
        db.send_create_signal(u'sense', ['PredicateObjectIndex'])

        # Adding unique constraint on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'prior']
        db.create_unique(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'prior'])

        # Adding unique constraint on 'PredicateObjectIndex', fields ['context', 'parent', 'prior', 'best_splitter']
        db.create_unique(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'prior', 'best_splitter'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'parent', 'prior']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'prior'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'prior']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'prior'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'prior']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'prior'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'prior']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'prior'])

        # Adding index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'prior']
        db.create_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'prior'])


    def backwards(self, orm):
        # Removing index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'prior']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'prior'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'prior']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'prior'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'predicate', 'object', 'prior']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'predicate_id', 'object_id', 'prior'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'prior']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'prior'])

        # Removing index on 'PredicateObjectIndex', fields ['context', 'parent', 'prior']
        db.delete_index(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'prior'])

        # Removing unique constraint on 'PredicateObjectIndex', fields ['context', 'parent', 'prior', 'best_splitter']
        db.delete_unique(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'prior', 'best_splitter'])

        # Removing unique constraint on 'PredicateObjectIndex', fields ['context', 'parent', 'predicate', 'object', 'prior']
        db.delete_unique(u'sense_predicateobjectindex', ['context_id', 'parent_id', 'predicate_id', 'object_id', 'prior'])

        # Removing index on 'Triple', fields ['inferred', 'deleted']
        db.delete_index(u'sense_triple', ['inferred', 'deleted'])

        # Removing index on 'Triple', fields ['predicate', 'object']
        db.delete_index(u'sense_triple', ['predicate_id', 'object_id'])

        # Removing unique constraint on 'Triple', fields ['subject', 'predicate', 'object']
        db.delete_unique(u'sense_triple', ['subject_id', 'predicate_id', 'object_id'])

        # Removing unique constraint on 'Context', fields ['name', 'parent', 'owner']
        db.delete_unique(u'sense_context', ['name', 'parent_id', 'owner_id'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'wordnet_id']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'wordnet_id'])

        # Removing unique constraint on 'Sense', fields ['source', 'word', 'pos', 'definition']
        db.delete_unique(u'sense_sense', ['source_id', 'word_id', 'pos', 'definition'])

        # Deleting model 'Source'
        db.delete_table(u'sense_source')

        # Deleting model 'Word'
        db.delete_table(u'sense_word')

        # Deleting model 'Example'
        db.delete_table(u'sense_example')

        # Deleting model 'Sense'
        db.delete_table(u'sense_sense')

        # Removing M2M table for field examples on 'Sense'
        db.delete_table(db.shorten_name(u'sense_sense_examples'))

        # Deleting model 'InferenceRule'
        db.delete_table(u'sense_inferencerule')

        # Deleting model 'Context'
        db.delete_table(u'sense_context')

        # Removing M2M table for field triples on 'Context'
        db.delete_table(db.shorten_name(u'sense_context_triples'))

        # Removing M2M table for field all_triples on 'Context'
        db.delete_table(db.shorten_name(u'sense_context_all_triples'))

        # Removing M2M table for field rules on 'Context'
        db.delete_table(db.shorten_name(u'sense_context_rules'))

        # Deleting model 'Triple'
        db.delete_table(u'sense_triple')

        # Removing M2M table for field inference_arguments on 'Triple'
        db.delete_table(db.shorten_name(u'sense_triple_inference_arguments'))

        # Deleting model 'PredicateObjectIndex'
        db.delete_table(u'sense_predicateobjectindex')


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
            'all_triples': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'contexts'", 'symmetrical': 'False', 'to': u"orm['sense.Triple']"}),
            'allow_inference': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'deleted': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'}),
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
            'Meta': {'unique_together': "(('subject', 'predicate', 'object'),)", 'object_name': 'Triple', 'index_together': "(('predicate', 'object'), ('inferred', 'deleted'))"},
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
            'po_hash': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'}),
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
            'trusted': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'db_index': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'auto_now': 'True', 'blank': 'True', 'auto_now_add': 'True', 'null': 'True', 'db_index': 'True'}),
            'wiktionary_id': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '700', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sense']