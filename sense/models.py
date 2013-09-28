import sys
import re
import math

from django.conf import settings
from django.db import models
from django.db.models import Sum, Count, Max
from django.utils import timezone
from django.db import connection
import django

import dtree

import constants as c
import settings as _settings

def print_status(top_percent, sub_percent, message, max_message_length=100, newline=False):
    """
    Updates the status "xxx.x% xxx.x% message" on the same console line.
    """
    if sub_percent is None:
        sys.stdout.write('\rStatus: %05.1f%% %s' % (
            float(top_percent),
            message[:max_message_length].ljust(max_message_length)
        ))
    else:
        sys.stdout.write('\rStatus: %05.1f%% %05.1f%% %s' % (
            float(top_percent),
            float(sub_percent),
            message[:max_message_length].ljust(max_message_length)
        ))
    if newline:
        sys.stdout.write('\n')
    sys.stdout.flush()

def walk_upwards(triple, priors=None, weight=None):
    """
    Iterates over each triple attached to the given triple's object via
    a transitive predicate.
    """
    if priors is None:
        priors = set()
    if weight is None:
        weight = triple.weight or 1.0
    #TODO:filter by context?
    #TODO:stop if weight gets too low?
    if triple in priors:
        return
    priors.add(triple)
    if not triple.predicate.transitive:
        return
    q = Triple.objects.real_active().filter(subject=triple.object, predicate=triple.predicate)
    for t1 in q.iterator():
        yield weight, t1
        for _ in walk_upwards(t1, priors=priors, weight=t1.weight*weight):
            yield _
            
def walk_downwards(triple, priors=None, weight=None):
    """
    Iterates over each triple attached to the given triple's subject via
    a transitive predicate.
    """
    if priors is None:
        priors = set()
    if weight is None:
        weight = triple.weight or 1.0
    #TODO:filter by context?
    #TODO:stop if weight gets too low?
    if triple in priors:
        return
    priors.add(triple)
    if not triple.predicate.transitive:
        return
    q = Triple.objects.real_active().filter(object=triple.subject, predicate=triple.predicate)
    for t1 in q.iterator():
#        if t1 in priors:
#            continue
        yield weight, t1
        for _ in walk_downwards(t1, priors=priors, weight=t1.weight*weight):
            yield _

class BaseModel(models.Model):
    
    created = models.DateTimeField(
        auto_now_add=True,
        blank=False,
        db_index=True,
        default=timezone.now,
        editable=False,
        null=False,
        help_text="The date and time when this record was created.")
        
    updated = models.DateTimeField(
        auto_now_add=True,
        auto_now=True,
        blank=True,
        db_index=True,
        default=timezone.now,
        editable=False,
        null=True,
        help_text="The date and time when this record was last updated.")
    
    deleted = models.DateTimeField(
        blank=True,
        db_index=True,
        null=True,
        help_text="The date and time when this record was deleted.")
    
    class Meta:
        abstract = True
        
    def clean(self, *args, **kwargs):
        """
        Called to validate fields before saving.
        Override this to implement your own model validation
        for both inside and outside of admin. 
        """
        super(BaseModel, self).clean(*args, **kwargs)
    
    #TODO:not necessary?
    #https://docs.djangoproject.com/en/dev/ref/models/instances/#django.db.models.Model.full_clean
#    def full_clean(self, *args, **kwargs):
#        return self.clean(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super(BaseModel, self).save(*args, **kwargs)

class SourceManager(models.Manager):
    
    def get_by_natural_key(self, name):
        return self.get(name=name)
    
class Source(BaseModel):
    
    objects = SourceManager()
    
    name = models.CharField(
        max_length=255,
        db_index=True,
        unique=True,
        blank=False,
        null=False)
    
    def natural_key(self):
        return (self.name,)
    
    def __unicode__(self):
        return self.name

class WordManager(models.Manager):

    def get_by_natural_key(self, text):
        return self.get(text=text)

class Word(BaseModel):
    """
    word = Word.objects.get(text='dog')
    for sense in word.senses.filter(pos=N):
        print sense.definition
    """
    
    objects = WordManager()
    
    text = models.CharField(
        max_length=700,
        db_index=True,
        unique=True,
        blank=False,
        null=False)
    
    wiktionary_id = models.CharField(
        max_length=700,
        blank=True,
        null=True,
        db_index=True,
        help_text='The slug used to identify this word on wiktionary.org.')
    
    sense_count = models.PositiveIntegerField(
        default=0,
        verbose_name='senses',
        editable=False,
        db_index=True)
    
    class Meta:
        ordering = ('text',)
    
    def natural_key(self):
        return (self.text,)
    
    def __unicode__(self):
        return self.text
    
    def save(self, *args, **kwargs):
        
        self.sense_count = self.senses.all().count()
        
        super(Word, self).save(*args, **kwargs)

class ExampleManager(models.Manager):

    def get_by_natural_key(self, text):
        return self.get_or_create(text=text)[0]

class Example(BaseModel):
    
    objects = ExampleManager()
    
    text = models.TextField(
        blank=False,
        null=False)
    
    def natural_key(self):
        return (self.text,)

class SenseManager(models.Manager):

    def get_by_natural_key(self, pos, source, word):
        return self.get(pos=pos, source=source, word=word)

class Sense(BaseModel):
    
    objects = SenseManager()
    
    source = models.ForeignKey(Source, related_name='senses', blank=True, null=True)
    
    word = models.ForeignKey(Word, related_name='senses')
    
    pos = models.CharField(
        max_length=5,
        default=c.N,
        choices=c.POS_CHOICES,
        db_index=True,
        blank=False,
        null=False,
        help_text='Part-of-speech.')
    
    wordnet_id = models.CharField(
        max_length=700,
        blank=True,
        null=True,
        db_index=True,
        help_text='The globally unique identifier of this sense in Wordnet.')
    
    language = models.CharField(max_length=2, blank=False, null=False, default='en')
    
    conceptnet_uri = models.URLField(max_length=700, blank=True, null=True)
    
    conceptnet_predicate = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text='The corresponding predicate name in ConceptNet.')
    
    transitive = models.NullBooleanField(
        help_text='If yes, implies that if A is B and B is C then A is C.')
    
    reverse_transitive = models.NullBooleanField(
        help_text='If yes, implies that if A is B then B is A.')
    
    #TODO:remove, deprecated?
    mutually_exclusive_subject_predicate = models.BooleanField(
        default=False,
        help_text='''If checked, implies that the subject, of any triple that
            uses this sense as a predicate, is mutually exclusive with any
            other predicate+object pair.<br/>
            e.g. The predicate IsA should be marked as such, since if "it" is
            a cat then "it" is not a dog.''')
    
    allow_predicate_usage = models.BooleanField(
        default=False,
        db_index=True,
        help_text='''If checked, this sense will be used for logical inferences
            with triples.''')
    
    definition = models.TextField(blank=True, null=True)
    
    examples = models.ManyToManyField(Example, blank=True, null=True)
    
    _name = models.CharField(
        max_length=700,
        verbose_name='name',
        editable=True,
        blank=True,
        null=True)
    
    class Meta:
        ordering = (
            'source',
            'pos',
            'word',
            'definition',
        )
        unique_together = (
            ('source', 'word', 'pos', 'definition'),
            ('source', 'word', 'pos', 'wordnet_id'),
        )
        
    def natural_key(self):
        return (self.pos,) \
            + self.source.natural_key() \
            + self.word.natural_key()
    natural_key.dependencies = ['sense.source', 'sense.word', 'sense.example']
    
    def save(self, *args, **kwargs):
        self.name
        
        if not (self.conceptnet_predicate or '').strip():
            self.conceptnet_predicate = None
        
        super(Sense, self).save(*args, **kwargs)
        
    @property
    def name(self):
        if self._name:
            return self._name
        desc = re.sub('[^a-zA-Z0-9\s\r\n]+', ' ', self.definition or '').strip()
        self._name = '%s.%s.%s.%s' % (self.source, self.pos, self.word, desc)
        self._name = re.sub('[^a-zA-Z0-9_\-\.]+', '_', self._name)[:700]
        self._name = re.sub('[_]+', '_', self._name)
        self._name = self._name.lower()
        return self._name
    
    def __unicode__(self):
        return '%s: %s' % (self.id, self.name)

class InferenceRule(BaseModel):
    
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        db_index=True)
    
    type = models.CharField(
        max_length=100,
        blank=False,
        choices=c.RULE_CHOICES,
        null=False,
        unique=True,
        db_index=True)
    
    def __unicode__(self):
        return self.name
    
    def get_isa_query(self, context, limit):
        cursor = connection.cursor()
        sql = '''
-- If A is B and B is C then A is C.
SELECT      t0.id AS A_id,
        t1.id AS C_id/*,
        t0.inferred_weight AS A_inferred_weight,
        t1.inferred_weight AS C_inferred_weight,
        t0.weight AS A_weight,
        t1.weight AS C_weight,
        t0.inference_depth AS A_inference_depth,
        t1.inference_depth AS C_inference_depth,
        t0.subject_id AS A,
        t1.object_id AS C
        */
FROM        sense_triple AS t0 -- A isa B
INNER JOIN  sense_context_all_triples AS sct0 ON
        sct0.triple_id = t0.id
    AND sct0.context_id = {context_id}
INNER JOIN  sense_sense AS pred0 ON
        pred0.id = t0.predicate_id
    AND pred0.conceptnet_predicate = 'IsA'
    AND pred0.transitive = true
    AND pred0.allow_predicate_usage = true
    AND t0.inference_depth < {maximum_inference_depth}
    AND (t0.inferred_weight IS NULL OR t0.inferred_weight >= {minimum_inference_weight})
    AND t0.deleted IS NULL
INNER JOIN  sense_triple AS t1 ON -- B isa C
        t1.predicate_id = t0.predicate_id
    AND t1.subject_id = t0.object_id
    AND t1.inference_depth < {maximum_inference_depth}
    AND (t1.inferred_weight IS NULL OR t1.inferred_weight >= {minimum_inference_weight})
    AND t1.deleted IS NULL
INNER JOIN  sense_context_all_triples AS sct1 ON
        sct1.triple_id = t1.id
    AND sct1.context_id = sct0.context_id
LEFT OUTER JOIN
        sense_triple AS t2 ON
        t2.subject_id = t0.subject_id
    AND t2.predicate_id = t0.predicate_id
    AND t2.object_id = t1.object_id
    AND t2.deleted IS NULL
LEFT OUTER JOIN
        sense_context_all_triples AS sct2 ON
        sct2.triple_id = t2.id
    AND sct2.context_id = sct1.context_id
WHERE       t2.id IS NULL OR sct2.id IS NULL
LIMIT {limit}
        '''.format(
            context_id=context.id,
            minimum_inference_weight=context.minimum_inference_weight,
            maximum_inference_depth=context.maximum_inference_depth,
            limit=limit,
        )
        #print sql
        cursor.execute(sql)
        return cursor
    
    def add_isa(self, row):
        """
        Creates the inferred triple for the arguments from the IsA rule.
        """

        at = Triple.objects.get(id=row['a_id'])
        ct = Triple.objects.get(id=row['c_id'])
        #print at
        #print ct
        
        # Create inferred triple.
        inference_depth = max(at.inference_depth, ct.inference_depth) + 1
        inferred_weight = at.effective_weight * ct.effective_weight
        newt, created = Triple.objects.get_or_create(
            subject=at.subject,
            predicate=at.predicate,
            object=ct.object,
            defaults=dict(
                inferred=True,
                inferred_weight=inferred_weight,
                inference_depth=inference_depth,
                inference_rule=self,
            )
        )
        
        # Use the highest weight, representing the most likely path.
        if created or newt.inferred_weight < inferred_weight \
        or (newt.inferred_weight == inferred_weight and newt.inference_depth > inference_depth):
            newt.inferred_weight = inferred_weight
            newt.inference_depth = inference_depth
            newt.inference_rule = self
            newt.inference_arguments.clear()
            newt.inference_arguments.add(at)
            newt.inference_arguments.add(ct)

        newt.save()
        #print newt
        return newt
    
    def infer(self, context, limit=None):
        """
        Creates triples in the given context according to the pre-defined rule.
        """
        limit = limit or 100000
        print 'Querying %i records...' % (limit,)
        if self.type == c.RULE_ISA:
            cursor = self.get_isa_query(context=context, limit=limit)
        else:
            raise NotImplementedError, \
                'Inference rule "%s" is not yet implemented.' % (self.type,)
                
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        django.db.transaction.enter_transaction_management()
        django.db.transaction.managed(True)
        i = 0
        try:
            while 1:
                
                desc = cursor.description
                row = cursor.fetchone()
                if not row:
                    print
                    print 'done'
                    break
                
                i += 1
                if not i % 10:
                    print_status(top_percent=i/float(limit)*100, sub_percent=None, message='')
                if not i % 1000:
                    print
                    print "Committing..."
                    django.db.transaction.commit()
                    
                row = dict(zip([col[0] for col in desc], row))
                #print 'row:', i, row
                
                if self.type == c.RULE_ISA:
                    newt = self.add_isa(row)
                else:
                    raise NotImplementedError
                    
                # Add it to the master context.
                context.add_triple(newt)
                
        finally:
            print "Committing..."
            settings.DEBUG = tmp_debug
            django.db.transaction.commit()
            django.db.transaction.leave_transaction_management()
            print "Committed."
        return i

class Context(BaseModel):
    
    name = models.CharField(max_length=200, blank=False, null=False, default='global')
    
    parent = models.ForeignKey('self', blank=True, null=True, related_name='children')
    
    top_parent = models.ForeignKey('self', blank=True, null=True, related_name='top_children')
    
    enabled = models.BooleanField(default=True)
    
    missing_truth_value = models.FloatField(
        default=c.NO,
        blank=False,
        null=False,
        help_text='''The truth value, in the range [0...1], assumed for triples that do not yet exist.<br/>
            A value of 0.0 implies a <a href="http://en.wikipedia.org/wiki/Closed_world_assumption" target="_blank">closed-world assumption</a>.<br/>
            Any other value implies an <a href="http://en.wikipedia.org/wiki/Open_world_assumption" target="_blank">open-world assumption</a>.'''
    )
    
    allow_inference = models.BooleanField(default=True)
    
    maximum_inference_depth = models.PositiveIntegerField(
        default=20,
        help_text='''The maximum level of nested inferences to make before
            further inference is stopped. This limit is necessary because
            without it, infinite number of inferences are possible.''')
    
    minimum_inference_weight = models.FloatField(
        default=0.01,
        help_text='''The minimum weight an inference can hold before it will
            no longer be used for further inferences.''')
    
    _triple_count = models.PositiveIntegerField(blank=True, null=True, db_column='triple_count', db_index=True)
    
    _inferred_triple_count = models.PositiveIntegerField(blank=True, null=True, db_column='inferred_triple_count', db_index=True)
    
    _subject_count = models.PositiveIntegerField(blank=True, null=True, db_column='subject_count', db_index=True)
    
    triples = models.ManyToManyField('Triple', related_name='direct_contexts')
    
    all_triples = models.ManyToManyField('Triple', related_name='contexts')
    
    fresh_all_triples = models.BooleanField(default=False)
    
    rules = models.ManyToManyField('InferenceRule', related_name='contexts')
    
    class Meta:
        unique_together = (
            ('name', 'parent'),
        )
        
    def __unicode__(self):
        if self.parent:
            return u'%s in %s' % (self.name, self.parent.name)
        return self.name
    
    def infer(self, *args, **kwargs):
        ret = False
        for rule in self.rules.all():
            print '-'*80
            print 'Rule:', rule
            ret = rule.infer(context=self, *args, **kwargs) or ret
        return ret
    
    def add_triple(self, t):
        # Add to direct list.
        self.triples.add(t)
        # Add to cached list.
        self.all_triples.add(t)
        # Add to all parents cached list.
        if self.top_parent:
            self.top_parent.all_triples.add(t)
            self.top_parent.clear_caches()
        self.clear_caches()
        
    def remove_triple(self, t):
        # Remove from direct list.
        self.triples.remove(t)
        # Remove from cached list.
        self.all_triples.remove(t)
        # Remove from all parents cached list.
        if self.top_parent:
            self.top_parent.all_triples.remove(t)
            self.top_parent.clear_caches()
        self.clear_caches()
    
    def refresh_triple_cache(self, save=False, clear=False, force=False):
        """
        Clears and regenerates the all_triples cache.
        """
        if self.fresh_all_triples and not force:
            return
        
        print 'refresh_all_triples:',self
        ThroughModel = self.all_triples.through # all_triples_id, context_id
    
        if clear:
            self.all_triples.clear()
        
        print 'Adding direct:', self
        q = self.triples.all()#.exclude(id__in=self.all_triples.all().values_list('id'))
        total = q.count()
        print 'total:',total
        i = 0
        for _ in q.iterator():
            i += 1
            if i == 1 or not i % 1000:
                print 'Adding direct triples (%i of %i)...' % (i, total)
            self.all_triples.add(_)
        #self.all_triples.add(q)
#            ThroughModel.objects.bulk_create(
#                ThroughModel(triple_id=t.pk, context_id=self.id)
#                for t in self.triples.all().exclude(id__in=self.all_triples.all().values_list('id')).iterator()
#            )
        
        for child in self.children.all():
            print 'Adding indirect:', child
            q = child.refresh_triple_cache(save=save, clear=clear, force=force)
            total = q.count()
            print 'total:',total
            i = 0
            for _ in q.iterator():
                i += 1
                if not i % 1000:
                    print 'Adding indirect triples (%i of %i)...' % (i, total)
                self.all_triples.add(_)
            #self.all_triples.add(q)
                
        self.fresh_all_triples = True
        self.save()
        print 'refresh_all_triples done!'
        return self.all_triples.all()
    
    def triple_count(self):
        if self._triple_count is None:
            self._triple_count = self.triples.filter(deleted__isnull=True).count() + sum(child.triple_count() for child in self.children.all())
            self.save()
        return self._triple_count
    
    def inferred_triple_count(self):
        print '='*80
        print 'inferred_triple_count...'
        if self._inferred_triple_count is None:
            print 'recalculating inferred_triple_count...'
            self._inferred_triple_count = self.triples.filter(inferred=True, deleted__isnull=True).count() + sum(child.inferred_triple_count() for child in self.children.all())
            self.save()
        return self._inferred_triple_count
    
    def subject_count(self):
        if self._subject_count is None:
            self._subject_count = self.triples.filter(deleted__isnull=True).aggregate(Count('subject', distinct=True))['subject__count'] + sum(child.subject_count() for child in self.children.all())
            self.save()
        return self._subject_count
    
    def get_top_parent(self):
        priors = set()
        p = self.parent or self
        while 1:
            priors.add(p)
            if p.parent and p.parent not in priors:
                p = p.parent
            else:
                return p
    
    def clear_caches(self):
        self._triple_count = None
        self._inferred_triple_count = None
        self._subject_count = None
        #self.fresh_all_triples = False
        self.save()
    
    def save(self, *args, **kwargs):
        
        self.missing_truth_value = min(max(self.missing_truth_value, c.NO), c.YES)
        
        if self.id:
            old = type(self).objects.get(id=self.id)
            if old.parent != self.parent:
                self.top_parent = None
                
        self.top_parent = self.get_top_parent()
        
        return super(Context, self).save(*args, **kwargs)

class TripleManager(models.Manager):
    
    def active(self, q=None):
        if q is None:
            q = self
        return q.filter(deleted__isnull=True)
    
    def real(self, q=None):
        if q is None:
            q = self
        return q.filter(inferred=False)
    
    def real_active(self, q=None):
        if q is None:
            q = self
        return self.active(q=self.real(q=q))

class Triple(BaseModel):
    
    objects = TripleManager()
    
    #context = models.ForeignKey(Context, related_name='triples')
    
    subject = models.ForeignKey(Sense, related_name='subject_triples')
    
    predicate = models.ForeignKey(Sense, related_name='predicate_triples')
    
    object = models.ForeignKey(Sense, blank=True, null=True, related_name='object_triples')
    
    conceptnet_uri = models.URLField(max_length=700, blank=True, null=True, db_index=True)
    
    conceptnet_weight = models.FloatField(blank=True, null=True)
    
    conceptnet_surface_text = models.CharField(max_length=7700, blank=True, null=True)
    
    conceptnet_id = models.CharField(max_length=200, blank=True, null=True, db_index=True)
    
    weight_sum = models.FloatField(
        default=0,
        blank=False,
        null=False,
        help_text='''Stores the summation of the numeric representation of
            a user\'s belief that this association is true.<br/>
            Yes=1, no=0, sometimes=0.5, rarely=0.1.''')
    
    weight_votes = models.PositiveIntegerField(
        default=0,
        verbose_name='votes',
        blank=False,
        null=False)
    
    weight = models.FloatField(
        blank=True,
        editable=False,
        db_index=True,
        null=True,
        help_text='''A number between [0...1] representing the relative
            probability or certainty of this triple being true.''')
    
    log_prob = models.FloatField(
        blank=True,
        editable=False,
        db_index=True,
        null=True,
        help_text='''The log() of the weight.''')
    
    total_contexts = models.PositiveIntegerField(
        default=0,
        db_index=True,
        blank=False,
        null=False)
    
    inferred = models.BooleanField(
        default=False,
        db_index=True,
        help_text='''If checked, indicates this triple was inferred by
            a predicate rule and was not directly added by a user.''')
    
    inference_depth = models.PositiveIntegerField(
        default=0,
        db_index=True,
        editable=False,
        blank=False,
        null=False,
        help_text='''The number of inferences that lead to this inference.
            If multiple inference paths lead to this inference, the minimum
            depth will be used.''')
    
    inferred_weight = models.FloatField(
        blank=True,
        editable=False,
        db_index=True,
        null=True,
        help_text='''A number between [0...1] representing the relative
            probability or certainty of this triple being true, used only
            for inferred triples that have no votes.''')
    
    inference_rule = models.ForeignKey(
        'InferenceRule',
        blank=True,
        null=True,
        help_text='''The rule used to infer this triple.''')
    
    inference_arguments = models.ManyToManyField(
        'self', blank=True, null=True,
        help_text='''The triples used by the inference rule
            to infer this triple.''')
    
    #TODO:remove, deprecated?
    subject_inferences_fresh = models.BooleanField(
        default=False,
        db_index=True,
        help_text='''If checked, indicates that inferences originating from
            the subject have been propagated. Otherwise, implies inferred
            triples need to be created, updated, or deleted.''')
    
    class Meta:
        unique_together = (
            ('subject', 'predicate', 'object'),
        )
        index_together = (
            ('predicate', 'object'),
            ('inferred', 'deleted'),
        )
    
    def __unicode__(self):
        #return '%s %s %s' % (self.subject, self.predicate, self.object)
        return self.natural_reading()
    
    def __repr__(self):
        return unicode(self)
    
    @property
    def effective_weight(self):
        if self.inferred:
            return self.inferred_weight
        return self.weight
    
    def natural_reading(self):
        """
        Phrases the triple as a natural language sentence.
        """
        format1 = '<qualifier> <subject> <predicate> <object>'
        format2 = '<subject> <qualifier> <predicate> <object>'
        format = format1
        #TODO:handle plurals
        #TODO:handle a/an
        if format == format1:
            weight = self.effective_weight or 0.0#self.contexts.all()[0].missing_truth_value
            if weight > (c.YES - c.MAYBE)/2.:
                pre = 'every'
            elif weight > (c.MAYBE - c.RARELY)/2.:
                pre = 'most'
            elif weight > (c.RARELY - c.NO)/2.:
                pre = 'few'
            else:
                pre = 'no'
            return u'%s %s %s %s' % (pre, self.subject.word.text, self.predicate.word.text, (self.object and self.object.word.text) or '')
        elif format == format2:
            weight = self.effective_weight or 0.0 #self.contexts.all()[0].missing_truth_value
            if weight > (c.YES - c.MAYBE)/2.:
                pre = 'every'
            elif weight > (c.MAYBE - c.RARELY)/2.:
                pre = 'most'
            elif weight > (c.RARELY - c.NO)/2.:
                pre = 'few'
            else:
                pre = 'no'
            return u'%s %s %s %s' % (self.subject.word.text, pre, self.predicate.word.text, (self.object and self.object.word.text) or '')
    
    def save(self, *args, **kwargs):
        
        if hasattr(self, 'votes'):
            ret = self.votes.all().aggregate(Sum('weight'))
            #print 'ret:',ret
            self.weight_sum = float(ret['weight__sum'] or 0)
            self.weight_votes = self.votes.all().count()
        
        if self.weight_votes:
            self.weight = self.weight_sum/self.weight_votes
        else:
            self.weight = None
        
        try:
            self.log_prob = math.log(self.weight)
        except TypeError:
            self.log_prob = None
        except ValueError:
            self.log_prob = None
        
        new = False
        if self.id:
            self.total_contexts = self.contexts.all().count()
            
            old = Triple.objects.get(id=self.id)
            if old.deleted != self.deleted:
                for ctx in self.contexts.all():
                    ctx.clear_caches()
        else:
            new = True
        
        super(Triple, self).save(*args, **kwargs)
        
        # Mark indexes as stale.
        PredicateObjectIndex.objects.filter(
            predicate=self.predicate,
            object=self.object,
            context__in=self.contexts.all(),
        ).update(fresh=False)
        
        if new:
            for ctx in self.contexts.all():
                ctx.clear_caches()

class BaseTripleVote(BaseModel):
    
    triple = models.ForeignKey(Triple, related_name='votes')
    
    #person = models.ForeignKey(Person, related_name='votes')
    
    weight = models.FloatField(
        choices=c.VOTE_CHOICES,
        blank=False,
        null=False,
        help_text='Degree of belief in triple. Yes=1, no=0, maybe=0.5, rarely=0.1.')
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        super(BaseTripleVote, self).save(*args, **kwargs)
        self.triple.save()

class PredicateObjectIndexPending(models.Model):

    id = models.CharField(
        max_length=200,
        primary_key=True,
        blank=False,
        null=False)
    
    context = models.ForeignKey(
        Context,
        on_delete=models.DO_NOTHING,
        db_column='context_id')
    
    predicate = models.ForeignKey(
        Sense,
        on_delete=models.DO_NOTHING,
        db_column='predicate_id',
        related_name='predicate_index_pending')
    
    object = models.ForeignKey(
        Sense,
        on_delete=models.DO_NOTHING,
        db_column='object_id',
        related_name='object_index_pending')
    
    subject_count_direct = models.PositiveIntegerField(
        blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'sense_predicateobjectindexpending'
    
    @classmethod
    def populate(cls, context=None, predicate=None):
        q = cls.objects.all()
        if context:
            q = q.filter(context=context)
        if predicate:
            q = q.filter(predicate__conceptnet_predicate=predicate)
        total = q.count()
        i = 0
        for r in q.iterator():
            i += 1
            if i == 1 or not i % 100:
                print 'Seeding %i of %i (%.2f%%)' % (i, total, i/float(total)*100)
            o, _ = PredicateObjectIndex.objects.get_or_create(
                context=r.context,
                predicate=r.predicate,
                object=r.object,
                subject_count_direct=r.subject_count_direct)
            #print o.id

class PredicateObjectIndexManager(models.Manager):
    
    def stale(self):
        return self.filter(fresh=False)
    
    def fresh(self):
        return self.filter(fresh=True)

#class PredicateObjectIndexLink(BaseModel):
#    
#    lower = models.ForeignKey(
#        'PredicateObjectIndex',
#        related_name='lower_poi_m2m')
#    
#    upper = models.ForeignKey(
#        'PredicateObjectIndex',
#        related_name='upper_poi_m2m')
#
#    entropy = models.FloatField(
#        blank=True,
#        null=True,
#        editable=False,
#        db_index=True,
#        help_text='''The entropy measure representing how much the
#            triple-store would be split using the lower-triple with respect
#            to the upper-triple.<br/>
#            A value close to 1.0 indicates a near-perfect split.<br/>
#            A value close to 0.0 indicates almost no split.''')
#    
#    class Meta:
#        unique_together = (
#            ('lower', 'upper'),
#        )
#        verbose_name = 'predicate object index layer'
#        verbose_name_plural = 'predicate object index layers'
#        
#    def save(self, *args, **kwargs):
#        
#        assert self.lower.predicate == self.upper.predicate
#        
#        # Note, we can only calculate an inter-POI entropy if the predicate
#        # implies mutual exclusivity of all matching subjects.
#        # e.g. If "it" isa cat then "it" can't also be a dog, so we can assume
#        # that whatever POI isa+cat and isa+dog share is a valid splitting
#        # criteria that we can calculate entropy for.
#        # Yet, if "it" has fur then "it" may also have a tail. Even if those
#        # two POI share a common abstraction, we can't assume one would be
#        # excluded by the other.
#        #
#        if self.lower.predicate.mutually_exclusive_subject_predicate \
#        and self.lower.subject_count_total and self.upper.subject_count_total:
#            self.entropy = dtree.entropy(data=dict(
#                a=self.lower.subject_count_total,
#                b=self.upper.subject_count_total,
#            ))
#        else:
#            self.entropy = 0
#        
#        return super(PredicateObjectIndexLink, self).save(*args, **kwargs)
    
class PredicateObjectIndex(BaseModel):
    
    objects = PredicateObjectIndexManager()
    
    parent = models.ForeignKey('self', blank=True, null=True)#, related_name='predicate_object_indexes')
    
    context = models.ForeignKey(Context, related_name='predicate_object_indexes')
    
    predicate = models.ForeignKey(Sense, related_name='predicate_index')
    
    object = models.ForeignKey(Sense, related_name='object_index')
    
    subject = models.ForeignKey(Sense, related_name='subject_index', blank=True, null=True)
    
    subject_count_direct = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        help_text='''Count of subjects directly linked to this predicate+object
            pair.''')
    
    subject_count_total = models.PositiveIntegerField(
        blank=True,
        null=True,
        db_index=True,
        help_text='''Total count of subjects linked to this predicate+object
            pair based on any inferences supported by the predicate.''')
    
    depth = models.PositiveIntegerField(
        blank=True,
        null=True,
        editable=False,
        db_index=True,
        help_text='This node\'s location in the decision tree. 0=top')
    
    entropy = models.FloatField(
        blank=True,
        null=True,
        db_index=True,
        help_text='''The entropy measure representing how much the
            triple-store would be split using the lower-triple with respect
            to the upper-triple.<br/>
            A value close to 1.0 indicates a near-perfect split.<br/>
            A value close to 0.0 indicates almost no split.''')
    
    fresh = models.BooleanField(
        default=False,
        db_index=True)
    
    best_splitter = models.NullBooleanField(
        db_index=True)
    
    _triple_ids = models.TextField(blank=True, null=True, db_column='triple_ids')
    
    @property
    def triple_ids(self):
        if not self._triple_ids:
            return []
        return map(int, self._triple_ids.split(','))
    
    @triple_ids.setter
    def triple_ids(self, lst):
        if lst:
            self._triple_ids = ','.join(map(str, lst))
        else:
            self._triple_ids = None
    
    class Meta:
        verbose_name_plural = 'predicate object indexes'
        ordering = ('-entropy',)
        unique_together = (
            ('context', 'subject', 'parent', 'predicate', 'object'),
            ('context', 'subject', 'best_splitter', 'depth'),
        )
        index_together = (
            ('context', 'parent', 'predicate', 'object', 'subject'),
            ('context', 'predicate', 'object', 'subject'),
            ('context', 'parent', 'predicate', 'object'),
            ('context', 'predicate', 'object'),
        )

    def __unicode__(self):
        return u'<PredicateObjectIndex: %s %s>' % (
            self.predicate.conceptnet_predicate,
            self.object.word.text,
        )

    def save(self, *args, **kwargs):
        
        if self.parent:
            self.depth = self.parent.depth
        else:
            self.depth = 0
        
        if self.id and self.entropy:
            old = type(self).objects.get(id=self.id)
            if self.entropy != old.entropy or self.best_splitter is None:
                best_entropy = type(self).objects\
                    .filter(subject=self.subject, depth=self.depth)\
                    .aggregate(Max('entropy'))['entropy__max']
                if best_entropy == self.entropy:
                    PredicateObjectIndex.objects.exclude(id=self.id)\
                        .filter(subject=self.subject, depth=self.depth)\
                        .update(best_splitter=None)
                    self.best_splitter = True
                else:
                    self.best_splitter = None
        
        super(PredicateObjectIndex, self).save(*args, **kwargs)
    
    @classmethod
    def update_all_best(cls):
        cursor = connection.cursor()
        cursor.execute('''
        SELECT m.subject_id, m.depth, m.max_entropy, n.id
        FROM (
            SELECT subject_id, depth, MAX(entropy) AS max_entropy
            FROM sense_predicateobjectindex AS poi
            GROUP BY subject_id, depth
            HAVING COUNT(best_splitter) <= 0
        ) AS m
        INNER JOIN sense_predicateobjectindex AS n
        ON    ((n.subject_id IS NULL AND m.subject_id IS NULL) OR (n.subject_id = m.subject_id))
        AND    n.depth = m.depth
        AND    n.entropy = m.max_entropy
        ''')
        for data in cursor.fetchall():
            #print subject_id, depth, max_entropy
            subject_id, depth, max_entropy, poi_id = data
            print data
            poi = cls.objects.get(id=poi_id)
            poi.save()
    
    def update(self, priors=None, depth=0):
        if priors is None:
            priors = set()
        if self.fresh:
            return self
        
        triple_ids = set()
        if self.parent:
            upper_total_subject_count = self.parent.subject_count_total
        else:
            upper_total_subject_count = self.context.subject_count()
        
        q2 = Triple.objects.real_active().filter(predicate=self.predicate, object=self.object)
        if not q2:
            self.subject_count_direct = self.subject_count_total = 0
            self.entropy = 0
            self.triple_ids = None
            self.fresh = True
            self.save()
            return self
        
        # Could all triples directly matching our predicate+object.
        agg = q2.distinct().aggregate(Count('id'))
        self.subject_count_direct = self.subject_count_total = agg['id__count']
        
        # Could all predicates indirectly matching our predicate+object
        # through a transitive predicate.
        # Recursively generate indexes to avoid redundant network searches.
        
        # PredicateObjectIndex objects connected "lower" in the network via
        # the subject of all triples that match the current predicate+object.
        #lowers = set()
        
        if self.predicate.transitive:
            for t2 in q2.iterator():
                triple_ids.add(t2.id)
                if t2 in priors:
                    continue
                priors.add(t2)
                q3 = Triple.objects.real_active().filter(predicate=t2.predicate, object=t2.subject)
                for t3 in q3.iterator():
                    triple_ids.add(t3.id)
                    if t3 in priors:
                        continue
                    priors.add(t3)
#                    print 'predicate:',self.predicate
#                    print 'object:',t3.object
                    poi3, _ = PredicateObjectIndex.objects.get_or_create(
                        context=self.context,
                        predicate=self.predicate,
                        object=t3.object)
                    poi3.update(priors=priors, depth=depth+1)
                    
#                    pois, _ = PredicateObjectIndexLink.objects.get_or_create(lower=poi3, upper=self)
#                    lowers.add(pois)
                    
                    #self.subject_count_total += poi3.subject_count_total
                    #self.subject_count_total += len(poi3.triple_ids)
                    triple_ids.update(poi3.triple_ids)
        
        self.triple_ids = triple_ids
        self.subject_count_total += len(triple_ids)
        if self.subject_count_total:
            self.entropy = dtree.entropy(data=dict(a=self.subject_count_total, b=upper_total_subject_count))
        else:
            self.entropy = 0
            
        self.fresh = True
        self.save()
            
        return self

    @classmethod
    def update_all(cls, predicate=None):
        q = cls.objects.stale()
        if predicate:
            q = q.filter(predicate__conceptnet_predicate=predicate)
        total = q.count()
        #TODO:filter by context?
        i = 0
        for poi in q.iterator():
            i += 1
            if i == 1 or not i % 100:
                print 'Updating %i of %i (%.2f%%)' % (i, total, i/float(total)*100)
            poi.update()
            