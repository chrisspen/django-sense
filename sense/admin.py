"""
Admin.
"""
from django.contrib import admin
from django.utils.safestring import mark_safe

import admin_steroids
from admin_steroids import formatters as f
from admin_steroids.filters import NullListFilter
from admin_steroids import utils

import models

class SourceAdmin(admin.ModelAdmin):
    pass
admin.site.register(models.Source, SourceAdmin)

class SenseInline(admin.StackedInline):
    model = models.Sense
    extra = 1
    max_num = 1
    
    exclude = (
        'examples',
        'deleted',
    )
    
    readonly_fields = (
        'subject_triples_link',
        'predicate_triples_link',
        'object_triples_link',
    )
    
    ordering = ('source', 'pos')
    
    def subject_triples_link(self, obj=None):
        try:
            if not obj or not obj.id:
                return ''
            q = obj.subject_triples.all()
            url = utils.get_admin_changelist_url(models.Triple) + ('?subject__id=%i' % obj.id)
            return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
        except Exception, e:
            return str(e)
    subject_triples_link.short_description = 'subject triples'
    
    def predicate_triples_link(self, obj=None):
        try:
            if not obj or not obj.id:
                return ''
            q = obj.predicate_triples.all()
            url = utils.get_admin_changelist_url(models.Triple) + ('?predicate__id=%i' % obj.id)
            return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
        except Exception, e:
            return str(e)
    predicate_triples_link.short_description = 'predicate triples'
    
    def object_triples_link(self, obj=None):
        try:
            if not obj or not obj.id:
                return ''
            q = obj.object_triples.all()
            url = utils.get_admin_changelist_url(models.Triple) + ('?object__id=%i' % obj.id)
            return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
        except Exception, e:
            return str(e)
    object_triples_link.short_description = 'object triples'

class WordAdmin(admin.ModelAdmin):
    search_fields = (
        'text',
    )
    list_display = (
        'id',
        'text',
        'sense_count',
        'text_length',
        'created',
    )
    list_filter = (
        'senses__pos',
        'senses__source',
        ('senses__conceptnet_predicate', NullListFilter),
        'senses__transitive',
        'senses__reverse_transitive',
    )
    readonly_fields = (
        'senses_link',
        'sense_count',
        'text_length',
        'wiktionary_link',
        #'subject_triples_link',
    )
    inlines = [SenseInline]
    
    def lookup_allowed(self, key, value=None):
        return True
    
    def wiktionary_link(self, obj=None):
        if not obj or not obj.wiktionary_id:
            return ''
        return mark_safe('<a href="http://en.wiktionary.org/wiki/%s" target="_blank"><input type="button" value="View" /></a>' % (obj.wiktionary_id, ))
    
    def senses_link(self, obj):
        q = obj.senses.all()
        url = utils.get_admin_changelist_url(models.Sense) + ('?word=%i' % obj.id)
        return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
    senses_link.short_description = 'senses'
    
admin.site.register(models.Word, WordAdmin)

class SenseExampleInline(admin.TabularInline):
    #model = models.Example
    model = models.Sense.examples.through
    extra = 0
    max_num = 0
    
    fields = (
        #'example__text',
        'example_text',
    )
    
    readonly_fields = (
        #'example__text',
        'example_text',
    )
    
    def example_text(self, obj):
        return obj.example.text
    
    def get_readonly_fields(self, request, obj=None):
        print [f.name for f in self.model._meta.fields]
        return list(self.readonly_fields) + [f.name for f in self.model._meta.fields]
    
class SenseAdmin(
    admin_steroids.options.BetterRawIdFieldsModelAdmin):
    search_fields = (
        'word__text',
    )
    list_filter = (
        'allow_predicate_usage',
        'pos',
        ('conceptnet_predicate', NullListFilter),
    )
    list_display = (
        'id',
        'name_short',
        'examples_count',
        'predicate_triples_link',
        'allow_predicate_usage',
    )
    readonly_fields = (
        'word',
        #'name',
        'examples_count',
        'subject_triples_link',
        'predicate_triples_link',
        'object_triples_link',
        '_text',
        'search_index',
    )
    exclude = (
        'examples',
    )
    
    actions = (
        'refresh',
    )
    
    inlines = [SenseExampleInline]
    
    def name_short(self, obj=None):
        if not obj:
            return ''
        return unicode(obj.name)[:100]
    
    def examples_count(self, obj):
        return obj.examples.all().count()
    examples_count.short_description = 'examples'
    
    def refresh(self, request, queryset):
        total = queryset.count()
        i = 0
        for c in queryset.iterator():
            i += 1
            print '%i of %i' % (i, total)
            c.save()
    refresh.short_description = 'Refresh selected %(verbose_name_plural)s'
    
    def lookup_allowed(self, key, value=None):
        return True
    
    def subject_triples_link(self, obj=None):
        try:
            if not obj or not obj.id:
                return ''
            q = obj.subject_triples.all()
            url = utils.get_admin_changelist_url(models.Triple) + ('?subject__id=%i' % obj.id)
            return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
        except Exception, e:
            return str(e)
    subject_triples_link.short_description = 'subject triples'
    
    def predicate_triples_link(self, obj=None):
        try:
            if not obj or not obj.id:
                return ''
            q = obj.predicate_triples.all()
            url = utils.get_admin_changelist_url(models.Triple) + ('?predicate__id=%i' % obj.id)
            return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
        except Exception, e:
            return str(e)
    predicate_triples_link.short_description = 'predicate triples'
    
    def object_triples_link(self, obj=None):
        try:
            if not obj or not obj.id:
                return ''
            q = obj.object_triples.all()
            url = utils.get_admin_changelist_url(models.Triple) + ('?object__id=%i' % obj.id)
            return mark_safe('<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
        except Exception, e:
            return str(e)
    object_triples_link.short_description = 'object triples'
    
admin.site.register(models.Sense, SenseAdmin)
    
class ContextAdmin(
    admin_steroids.options.BetterRawIdFieldsModelAdmin,
    admin_steroids.options.FormatterModelAdmin):
    
    search_fields = (
        'name',
    )
    list_filter = (
        'allow_inference',
        'owner',
    )
    list_display = (
        'id',
        'name',
        'parent',
        'owner',
        'accessibility',
        'editability',
        'triple_count',
        'subject_count',
        'allow_inference',
        'inferred_triple_count',
    )
    readonly_fields = (
        'triple_count',
        'inferred_triple_count',
        'subject_count',
        'created',
        'updated',
        'deleted',
    )
    exclude = (
        'triples',
        'all_triples',
        'senses',
        'all_senses',
    )
    raw_id_fields = (
        'parent',
        'rules',
        'owner',
        'top_parent',
    )
    
    actions = (
        'refresh_all_triples',
    )
    
    def lookup_allowed(self, key, value=None):
        return True
    
    def refresh_all_triples(self, request, queryset):
        total = queryset.count()
        i = 0
        for c in queryset.iterator():
            i += 1
            print '%i of %i' % (i, total)
            c.fresh_all_triples = False
            c.save()
    refresh_all_triples.short_description = 'Mark total triple list for selected %(verbose_name_plural)s as stale'
    
admin.site.register(models.Context, ContextAdmin)

class TripleFlowAdmin(
    admin_steroids.options.BetterRawIdFieldsModelAdmin,
    admin_steroids.options.FormatterModelAdmin):
    
    list_display = (
        'id',
        'context',
        'parent_str',
        'triple_str',
        'index',
        'rindex',
        'depth',
        'deleted',
    )
    list_filter = (
        ('deleted', NullListFilter),
    )
    
    raw_id_fields = (
        'context',
        'parent',
        'triple',
    )
    readonly_fields = (
        'parent_str',
        'triple_str',
    )
    
    def parent_str(self, obj=None):
        if not obj or not obj.parent:
            return ''
        s = obj.parent.triple.text().strip()
        if len(s) > 50:
            s = s[:47] + '...'
        return '%i: %s' % (obj.parent.triple.id, s)
    parent_str.short_description = 'parent'
    
    def triple_str(self, obj=None):
        if not obj:
            return ''
        s = obj.triple.text().strip()
        if len(s) > 100:
            s = s[:(100-3)] + '...'
        return '%i: %s' % (obj.triple.id, s)
    triple_str.short_description = 'triple'
    
admin.site.register(models.TripleFlow, TripleFlowAdmin)

class TripleAdmin(
    admin_steroids.options.BetterRawIdFieldsModelAdmin,
    admin_steroids.options.FormatterModelAdmin):
    
    search_fields = (
        'subject__word__text',
        'predicate__word__text',
        'object__word__text',
        '_text',
    )
    list_filter = (
        'inferred',
        ('deleted', NullListFilter),
    )
    list_display = (
        'id',
        #'context',
        'subject_link',
        'predicate_link',
        'object_link',
        'weight',
        'weight_votes',
        'total_contexts',
        'inferred',
        'inference_depth',
        'inferred_weight',
        'created',
        'deleted',
    )
    raw_id_fields = (
        'owner',
        'subject',
        'subject_triple',
        'predicate',
        'object',
        'object_triple',
        'inference_rule',
        'inference_arguments',
    )
    readonly_fields = (
        'natural_reading',
        'subject_link',
        'predicate_link',
        'object_link',
        'po_hash',
        '_text',
        'search_index',
    )
    exclude = (
    )
    
    actions = (
        'refresh',
    )
    
    def lookup_allowed(self, key, value=None):
        return True
    
    def refresh(self, request, queryset):
        total = queryset.count()
        i = 0
        for c in queryset.iterator():
            i += 1
            print '%i of %i' % (i, total)
            c.save()
    refresh.short_description = 'Refresh selected %(verbose_name_plural)s'
    
    def subject_link(self, obj=None):
        if not obj:
            return ''
        if obj.subject:
            url = utils.get_admin_change_url(obj.subject.word)
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.subject)[:50].replace(' ', '&nbsp;')))
        elif obj.subject_triple:
            url = utils.get_admin_change_url(obj.subject_triple)
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.subject_triple)[:50].replace(' ', '&nbsp;')))
        return ''
    subject_link.short_description = 'subject'
    
    def predicate_link(self, obj=None):
        if not obj:
            return ''
        url = utils.get_admin_change_url(obj.predicate.word)
        return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.predicate)[:50].replace(' ', '&nbsp;')))
    predicate_link.short_description = 'predicate'
    
    def object_link(self, obj=None):
        if not obj:
            return ''
        if obj.object:
            url = utils.get_admin_change_url(obj.object.word)
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.object)[:50].replace(' ', '&nbsp;')))
        elif obj.object_triple:
            url = utils.get_admin_change_url(obj.object_triple)
            return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.object_triple)[:50].replace(' ', '&nbsp;')))
        return ''
    object_link.short_description = 'object'
    
admin.site.register(models.Triple, TripleAdmin)

class PredicateObjectIndexAdmin(
    admin_steroids.options.BetterRawIdFieldsModelAdmin,
    admin_steroids.options.FormatterModelAdmin):
    
    list_display = (
        'id',
        'context',
        #'predicate',
        'predicate_link',
        #'object',
        'object_link',
        'parent',
        'prior',
        'best_splitter',
        'subject_count_total',
        'depth',
        'entropy',
        'fresh',
        'enabled',
    )
    
    list_filter = (
        'fresh',
        'enabled',
        'best_splitter',
        ('entropy', NullListFilter),
    )
    
    raw_id_fields = (
        'context',
        'predicate',
        'object',
        'parent',
    )
    
    readonly_fields = (
        'children_link',
    )
    
    exclude = (
        '_triple_ids',
    )
    
    def lookup_allowed(self, key, value=None):
        return True
    
    def predicate_link(self, obj=None):
        if not obj:
            return ''
        url = utils.get_admin_change_url(obj.predicate.word)
        return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.predicate)[:50].replace(' ', '&nbsp;')))
    predicate_link.short_description = 'predicate'
    
    def object_link(self, obj=None):
        if not obj:
            return ''
        url = utils.get_admin_change_url(obj.object.word)
        return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.object)[:50].replace(' ', '&nbsp;')))
    object_link.short_description = 'object'
    
    def children_link(self, obj=None):
        if not obj:
            return ''
        q = obj.children.all()
        url = utils.get_admin_changelist_url(models.PredicateObjectIndex) + '?parent__id=' + str(obj.id)
        return mark_safe(u'<a href="%s" target="_blank"><input type="button" value="View %i" /></a>' % (url, q.count()))
    children_link.short_description = 'children'
    
admin.site.register(models.PredicateObjectIndex, PredicateObjectIndexAdmin)

class InferenceRuleAdmin(admin.ModelAdmin):
    
    list_display = (
        'name',
        'type',
    )
    
    readonly_fields = (
        'created',
        'updated',
        'deleted',
        'search_index',
    )
    
admin.site.register(models.InferenceRule, InferenceRuleAdmin)

class TripleInferenceAdmin(
    admin_steroids.options.BetterRawIdFieldsModelAdmin):
    
    list_display = (
        'id',
        'inference_rule',
        'inferred_triple',
        'inference_arguments_str',
        'confirmed',
    )
    
    readonly_fields = (
        'inference_arguments_str',
        #'confirmed',
    )
    
    raw_id_fields = (
        'inference_rule',
        'inferred_triple',
        'inference_arguments',
    )
    
    list_filter = (
        'confirmed',
    )
    
    def inference_arguments_str(self, obj=None):
        if not obj:
            return ''
        return ', '.join(_._text for _ in obj.inference_arguments.all())
    inference_arguments_str.short_description = 'arguments'
    
admin.site.register(models.TripleInference, TripleInferenceAdmin)
