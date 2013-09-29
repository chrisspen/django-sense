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
    
class SenseAdmin(admin.ModelAdmin):
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
    )
    exclude = (
        'examples',
    )
    inlines = [SenseExampleInline]
    
    def name_short(self, obj=None):
        if not obj:
            return ''
        return unicode(obj.name)[:100]
    
    def examples_count(self, obj):
        return obj.examples.all().count()
    examples_count.short_description = 'examples'
    
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
    
class ContextAdmin(admin.ModelAdmin):
    search_fields = (
        'name',
    )
    list_filter = (
        'allow_inference',
    )
    list_display = (
        'id',
        'name',
        'parent',
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
    )
    raw_id_fields = (
        'parent',
        'rules',
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

class TripleAdmin(
    admin_steroids.BetterRawIdFieldsModelAdmin,
    admin_steroids.FormatterModelAdmin):
    
    search_fields = (
        'subject__word__text',
        'predicate__word__text',
        'object__word__text',
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
        'subject',
        'predicate',
        'object',
        'inference_rule',
        'inference_arguments',
    )
    readonly_fields = (
        'natural_reading',
        'subject_link',
        'predicate_link',
        'object_link',
    )
    exclude = (
    )
    
    def lookup_allowed(self, key, value=None):
        return True
    
    def subject_link(self, obj=None):
        if not obj:
            return ''
        url = utils.get_admin_change_url(obj.subject.word)
        return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.subject)[:50].replace(' ', '&nbsp;')))
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
        url = utils.get_admin_change_url(obj.object.word)
        return mark_safe(u'<a href="%s" target="_blank">%s</a>' % (url, unicode(obj.object)[:50].replace(' ', '&nbsp;')))
    object_link.short_description = 'object'
    
admin.site.register(models.Triple, TripleAdmin)

class PredicateObjectIndexToSelfAdmin(
    admin_steroids.BetterRawIdFieldsModelAdmin,
    admin_steroids.FormatterModelAdmin):
    
    list_display = (
        'lower',
        'upper',
        'entropy',
        'created',
        'updated',
    )
    raw_id_fields = (
        'lower',
        'upper',
    )
    readonly_fields = (
        'entropy',
        'created',
        'updated',
    )
    
#admin.site.register(models.PredicateObjectIndexToSelf, PredicateObjectIndexToSelfAdmin)
    
class PredicateObjectIndexAdmin(
    admin_steroids.BetterRawIdFieldsModelAdmin,
    admin_steroids.FormatterModelAdmin):
    
    list_display = (
        'id',
        'context',
        #'predicate',
        'predicate_link',
        #'object',
        'object_link',
        'subject',
        'parent',
        'best_splitter',
        'subject_count_direct',
        'subject_count_total',
        'depth',
        'entropy',
        'fresh',
    )
    
    list_filter = (
        'fresh',
        'best_splitter',
        ('entropy', NullListFilter),
    )
    
    raw_id_fields = (
        'context',
        'predicate',
        'object',
        'subject',
        'parent',
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
    )
    
admin.site.register(models.InferenceRule, InferenceRuleAdmin)