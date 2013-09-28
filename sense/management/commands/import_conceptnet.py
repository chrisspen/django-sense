#!/usr/bin/python
import datetime
import os
import random
import re
import sys
import time
import csv
from optparse import make_option
from collections import namedtuple

#http://pythonadventures.wordpress.com/tag/ascii/
reload(sys)
sys.setdefaultencoding("utf-8")

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core import serializers
import django
from django.utils.encoding import smart_text, smart_unicode

from sense import models
from sense import constants as c
from sense import settings as _settings

def camelcase_to_underscore(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

PredicateProcessor = namedtuple('PredicateProcessor', ['xpos', 'ypos', 'create_sense'])

predicate_processors = dict(
    AtLocation=PredicateProcessor(xpos='n', ypos='n', create_sense=True),
    CapableOf=PredicateProcessor(xpos='n', ypos='v', create_sense=True),
    Causes=PredicateProcessor(xpos='nv', ypos='nv', create_sense=False),
    CausesDesire=PredicateProcessor(xpos='nv', ypos='nv', create_sense=False),
    ConceptuallyRelatedTo=PredicateProcessor(xpos='nv', ypos='nvar', create_sense=False),
    CreatedBy=PredicateProcessor(xpos='n', ypos='nv', create_sense=False),
    DefinedAs=PredicateProcessor(xpos='n', ypos='n', create_sense=True),
    Derivative=PredicateProcessor(xpos='n', ypos='nv', create_sense=False),
    DerivedFrom=PredicateProcessor(xpos='n', ypos='nv', create_sense=False),
    DesireOf=PredicateProcessor(xpos='n', ypos='nv', create_sense=False),
    Desires=PredicateProcessor(xpos='n', ypos='nv', create_sense=False),
    Entails=PredicateProcessor(xpos='v', ypos='v', create_sense=True),
)

class URI(object):
    
    def __init__(self):
        self.first = None
        self.lang = None
        self.word_slug = None
        self.pos = None
        self.sense_slug = None
    
    @classmethod
    def fromstring(cls, s):
        s = smart_unicode(s, errors='replace')
        parts = [_.strip() for _ in s.split('/') if _.strip()]
        self = URI()
        if parts:
            self.first = parts[0]
        if len(parts) >= 2:
            self.lang = parts[1]
        if len(parts) >= 3:
            self.word_slug = parts[2]
        if len(parts) >= 4:
            self.pos = parts[3]
        if len(parts) >= 5:
            self.sense_slug = parts[4]
        return self
    
    @property
    def clean_sense_slug(self):
        return re.sub('[^a-zA-Z0-9_\-]+', '', self.sense_slug or '')
    
    @property
    def word_text(self):
        return self.word_slug and self.word_slug.replace('_', ' ')
    
    def get_native_sense(self, create=False):
        q = models.Sense.objects.filter(
            language=self.lang,
            word__text=self.word_text,
            pos=self.pos,
            _name__icontains=self.clean_sense_slug)
        if q.count():
            return q
        q = models.Sense.objects.filter(
            language=self.lang,
            word__text=self.word_text,
            _name__icontains=self.clean_sense_slug)
        if q.count() == 1:
            return q
        q = models.Sense.objects.filter(
            language=self.lang,
            word__text=self.word_text)
        if q.count() == 1:
            return q
        
        if create and self.pos in 'nvar':
            word, _ = models.Word.objects.get_or_create(text=self.word_text)
            sense, _ = models.Sense.objects.get_or_create(
                word=word,
                pos=self.pos,
                language=self.lang,
                definition=self.clean_sense_slug)
            word.save()
            return models.Sense.objects.filter(id=sense.id)
        
        return models.Sense.objects.filter(id=0)
    
    @property
    def has_native_sense(self):
        if not self.is_complete:
            return False
        return bool(self.get_native_sense().count())
    
    @property
    def is_complete(self):
        return bool(self.first and self.lang and self.word_slug and self.pos and self.sense_slug)
    
    def __unicode__(self):
        if not self.pos:
            u = u'/%s/%s/%s' % (self.first, self.lang, self.word_slug)
        elif not self.sense_slug:
            u = u'/%s/%s/%s/%s' % (self.first, self.lang, self.word_slug, self.pos)
        else:
            u = u'/%s/%s/%s/%s/%s' % (self.first, self.lang, self.word_slug, self.pos, self.sense_slug)
        return smart_unicode(u)
    
    def __str__(self):
        return unicode(self)
    
    def __repr__(self):
        return unicode(self)

#NOTE:experimental
class Command(BaseCommand):
    help = 'Import definitions from ConceptNet.'
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('--dryrun',
            action='store_true',
            dest='dryrun',
            default=False,
            help='If given, does not commit any changes.'),
        make_option('--context',
            dest='context',
            default='conceptnet',
            help='The default context to link all created relations to.'),
        make_option('--max_words',
            dest='max_words',
            default=0,
            help='The maximum number of words to process. Default is all words.'),
        make_option('--i',
            dest='start_i',
            default=0,
            help='The index of the first word to start processing.'),
        make_option('--csv',
            dest='csv',
            default=None,
            help='The filename of the bulk CSV file to process.'),
        make_option('--onlypreds',
            dest='onlypreds',
            action='store_true',
            default=False,
            help='If given, only outputs a set of unique predicates found.'),
        make_option('--verbose',
            dest='verbose',
            action='store_true',
            default=False,
            help='If given, outputs debugging info for each row processed.'),
        make_option('--step',
            dest='step',
            action='store_true',
            default=False,
            help='If given, waits for user input after processing each row.'),
        make_option('--complete',
            dest='complete',
            default='1',
            help='Filters triples by completeness. A triple is complete if it contains part-of-speech and sense-slug.'),
        make_option('--lang',
            dest='lang',
            default='en',
            help='The language to target. All senses linked to other languages will be ignored.'),
        make_option('--pred',
            dest='pred',
            default='',
            help='The predicate to filter by.'),
        )
    
    def handle(self, *args, **options):
        dryrun = options['dryrun']
        start_i = int(options['start_i'])
        max_words = int(options['max_words'])
        step = options['step']
        verbose = options['verbose']
        csv_fn = options['csv']
        lang = options['lang']
        complete = options['complete']
        target_predicate = options['pred']
        
        fields = 'uri,rel,start,end,context,weight,sources,id,dataset,surfaceText'.split(',')
        data = None
        total = 0
        if csv_fn:
            assert os.path.isfile(csv_fn)
            data = csv.reader(open(csv_fn), delimiter='\t')
            total = open(csv_fn).read().count('\n')
        assert data, 'No data source specified.'
        
        context = options['context']
        if context.isdigit():
            context = models.Context.objects.get(id=options['context'])
        else:
            context, _ = models.Context.objects.get_or_create(name=options['context'])
        
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        django.db.transaction.enter_transaction_management()
        django.db.transaction.managed(True)
        words_processed = 0
        
        voter = _settings.get_default_person
        if voter:
            voter = voter()
            
        preds = set()
        i = 0
        commit_freq = 100
        skipped = 0
        triples_created = 0
        from pprint import pprint
        try:
            for row in data:
                i += 1
                words_processed += 1
                if start_i and i < start_i:
                    continue
                
                if not i % 1000:
                    print '%i of %i' % (i, total)
                    
                if not i % commit_freq and not dryrun:
                    print "Committing..."
                    django.db.transaction.commit()
                
                row = dict(zip(fields, row))
                
                start_uri = URI.fromstring(row['start'])
                end_uri = URI.fromstring(row['end'])
                
                if start_uri.lang != lang or end_uri.lang != lang:
                    # Ignore languages we're not interested in.
                    skipped += 1
                    continue
                elif complete == '1' and (not start_uri.is_complete or not end_uri.is_complete):
                    # Ignore incomplete triples if we're only looking for completes.
                    skipped += 1
                    continue
                elif complete == '0' and (start_uri.is_complete and end_uri.is_complete):
                    # Ignore complete triples if we're only looking for incompletes.
                    skipped += 1
                    continue
                
                if options['onlypreds']:
                    preds.add(row['rel'])
                else:
                    
                    rel = row['rel']
                    
#                    if rel in (
#                        '/r/Antonym',#C
#                        '/r/AtLocation',#C
#                        #'/r/Attribute',#C
#                        #'/r/CapableOf',#NC
#                        #'/r/Causes',
##                        '/r/CausesDesire', '/r/ConceptuallyRelatedTo', '/r/CreatedBy', '/r/DefinedAs',
##                        '/r/Derivative', '/r/DerivedFrom', '/r/DesireOf', '/r/Desires', '/r/Entails',
##                        '/r/HasA',
#                        ):
#                        continue#TODO:remove
                    
                    predicate = rel.split('/')[-1]
                    
                    if target_predicate and predicate != target_predicate:
                        skipped += 1
                        continue
                    
                    predicate_desc = camelcase_to_underscore(predicate).lower().replace('_', ' ')
                    predicate_senses = models.Sense.objects.filter(conceptnet_predicate=predicate)
                    if predicate_senses.count():
                        predicate_sense = predicate_senses[0]
                    else:
                        predicate_word, _ = models.Word.objects.get_or_create(text=predicate_desc)
                        predicate_sense, _ = models.Sense.objects.get_or_create(
                            word=predicate_word,
                            language=start_uri.lang,
                            conceptnet_predicate=predicate,
                            defaults=dict(
                                pos=c.V,
                                definition=predicate_desc,
                            )
                        )
                        predicate_word.save()
                    
                    if verbose:
                        pprint(row)
                        print 'start:',start_uri,'complete:',start_uri.is_complete,'native:',start_uri.has_native_sense
                        print 'predicate:',predicate_sense
                        print 'end:',end_uri,'complete:',end_uri.is_complete,'native:',end_uri.has_native_sense
                    
                    if start_uri.is_complete and end_uri.is_complete:
                        # Add triples that cleanly map to our Wordnet-based senses.
                        if start_uri.has_native_sense and end_uri.has_native_sense:
                            triple, triple_created = models.Triple.objects.get_or_create(
                                subject=start_uri.get_native_sense(create=True)[0],
                                predicate=predicate_sense,
                                object=end_uri.get_native_sense(create=True)[0],
                            )
                            triples_created += triple_created
                            triple.conceptnet_id = row['id']
                            if row['surfaceText']:
                                triple.conceptnet_surface_text = row['surfaceText']
                            triple.save()
                            context.triples.add(triple)
                            if _settings.TripleVoteModel and voter:
                                _settings.TripleVoteModel.objects.get_or_create(
                                    triple=triple,
                                    person=voter,
                                    weight=c.YES if float(row['weight']) > 0 else c.NO)
                    else:
                        # Attempt to deduce senses from Conceptnet nodes that have no sense.
                        pp = predicate_processors[predicate]
                        todo
                    
                    if step:
                        raw_input('<enter>')
            
            if options['onlypreds']:
                print '-'*80
                for pred in sorted(preds):
                    print pred
            
        finally:
            if not dryrun:
                print "Committing..."
                settings.DEBUG = tmp_debug
                django.db.transaction.commit()
                django.db.transaction.leave_transaction_management()
                print "Committed."
            print '%i rows processed.' % (words_processed,)
            print '%i rows skipped.' % (skipped,)
            print '%i triples created.' % (triples_created,)
            