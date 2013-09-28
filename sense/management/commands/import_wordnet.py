#!/usr/bin/python
import datetime
import os
import sys
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
import django

try:
    from nltk.corpus import wordnet as wn
except ImportError:
    if raw_input('Download Wordnet? (y/n): ').lower().strip() == 'y':
        import nltk; nltk.download('wordnet')
        from nltk.corpus import wordnet as wn
    else:
        print>>sys.stderr, 'Wordnet not installed. Please download Wordnet '\
            'into NLTK\'s local data repository.'
        raise

from sense import models
from sense import constants as c
from sense import settings as _settings

def plural(word):
    """
    Converts a word to its plural form.
    
    http://en.wikipedia.org/wiki/English_plural#Defective_nouns
    http://english.stackexchange.com/questions/45039/is-there-a-term-for-words-that-have-identical-singular-and-plural-forms
    http://web2.uvcs.uvic.ca/elc/studyzone/330/grammar/irrplu.htm
    """
    #TODO:handle all plurale tantums?
    if word in c.PLURALE_TANTUMS:
        # defective nouns
        return word
    elif word in c.IRREGULAR_NOUNS:
        return c.IRREGULAR_NOUNS[word]
    elif word.endswith('fe'):
        # wolf -> wolves
        return word[:-2] + 'ves'
    elif word.endswith('f'):
        # knife -> knives
        return word[:-1] + 'ves'
    elif word.endswith('o'):
        # potato -> potatoes
        return word + 'es'
    elif word.endswith('us'):
        # cactus -> cacti
        return word[:-2] + 'i'
    elif word.endswith('on'):
        # criterion -> criteria
        return word[:-2] + 'a'
    elif word.endswith('y'):
        # community -> communities
        return word[:-1] + 'ies'
    elif word[-1] in 'sx' or word[-2:] in ['sh', 'ch']:
        return word + 'es'
    elif word.endswith('an'):
        return word[:-2] + 'en'
    else:
        return word + 's'

def add_word(synset, context, source=None, add_relations=True, voter=None, word_text=None):
    assert isinstance(context, models.Context), 'Invalid context: %s' % (context,)
    #context = context or models.Context.objects.get(name='global', parent__isnull=True)

    if word_text:
        # Create a unique ID for synonyms.
        wordnet_id = synset.name + '.' + word_text
    else:
        wordnet_id = synset.name

    word_text = word_text or synset.name
    word_text = word_text.split('.')[0].strip().replace('_', ' ')
    print 'Adding word %s (%s)...' % (word_text, synset.name)
    #TODO:interpret ADJ_SAT as ADJ?
    pos = c.WN_POS_TO_LOCAL_POS.get(synset.pos)
    if not pos:
        return None, None
    print 'word_text:',word_text
    if not word_text:
        return None, None
    word, _ = models.Word.objects.get_or_create(text=word_text)
    
    # Import sense.
    
    try:
        sense, _ = models.Sense.objects.get_or_create(
            wordnet_id=wordnet_id,
            defaults=dict(
                source=source,
                word=word,
                pos=pos,
                definition=synset.definition,
            )
        )
        sense.definition = synset.definition
        sense.save()
    except ValidationError, e:
        q = models.Sense.objects.filter(wordnet_id=wordnet_id)
        if q.count():
            sense = q[0]
        else:
            print>>sys.stderr, 'Error: %s' % (e,)
            return None, None
    
    # Import examples.
    for example_text in synset.examples:
        ex, _ = models.Example.objects.get_or_create(text=example_text)
        sense.examples.add(ex)
    
#    print '_settings.TripleVoteModel:',_settings.TripleVoteModel
#    print 'voter:',voter
    
    if add_relations:
        print 'Adding relations...'
        
        SAMEAS = models.Sense.objects.get(pos=c.V, word__text=c.SAMEAS)
        ISOPPOSITEOF = models.Sense.objects.get(pos=c.V, word__text=c.ISOPPOSITEOF)
        ISA = models.Sense.objects.get(pos=c.V, word__text=c.ISA)
        ISPARTOF = models.Sense.objects.get(pos=c.ADJ, word__text=c.ISPARTOF)
        HAS_PLURAL = models.Sense.objects.get(pos=c.ADJ, word__text=c.HAS_PLURAL)
        HAS_SINGULAR = models.Sense.objects.get(pos=c.ADJ, word__text=c.HAS_SINGULAR)
        
        # Create plurality links.
        if _settings.TripleVoteModel and voter and synset.pos == c.N:
            
            word_lemma = wn.morphy(word_text)
            if word_lemma == word_text:
                # Current word is likely the singular or an irregular noun.
                word_text_p = plural(word_text)
                other_word, other_sense = add_word(synset=synset, word_text=word_text_p, add_relations=False, source=source, context=context, voter=voter)
                if other_word:
                    
                    triple, _ = models.Triple.objects.get_or_create(subject=sense, predicate=HAS_PLURAL, object=other_sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                    
                    triple, _ = models.Triple.objects.get_or_create(subject=other_sense, predicate=HAS_SINGULAR, object=sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                
            else:
                # Current word is likely plural or an irregular noun.
                word_text_s = word_lemma
                other_word, other_sense = add_word(synset=synset, word_text=word_text_s, add_relations=False, source=source, context=context, voter=voter)
                if other_word:
                    
                    triple, _ = models.Triple.objects.get_or_create(subject=sense, predicate=HAS_SINGULAR, object=other_sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                    
                    triple, _ = models.Triple.objects.get_or_create(subject=other_sense, predicate=HAS_PLURAL, object=sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
        
        # Create synonyms.
        sameas_added = 0
        if _settings.TripleVoteModel and voter:
            for lemma in synset.lemmas:
                sameas_added += 1
                print 'lemma:',lemma
                other_word, other_sense = add_word(synset=synset, word_text=lemma.name, add_relations=False, source=source, context=context, voter=voter)
                if other_word:
                    triple, _ = models.Triple.objects.get_or_create(subject=other_sense, predicate=SAMEAS, object=sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                    triple, _ = models.Triple.objects.get_or_create(subject=sense, predicate=SAMEAS, object=other_sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
        print 'Added %i same-as relations.' % (sameas_added,)
        
        # Create antonyms.
        antonyms_added = 0
        if _settings.TripleVoteModel and voter:
            for lemma in synset.lemmas:
                for antonym_lemma in lemma.antonyms():
                    antonyms_added += 1
                    antonym_synset = antonym_lemma.synset
                    other_word, other_sense = add_word(synset=antonym_synset, add_relations=False, source=source, context=context, voter=voter)
                    if not other_word:
                        continue
                    
                    triple, _ = models.Triple.objects.get_or_create(subject=sense, predicate=ISOPPOSITEOF, object=other_sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                    
                    triple, _ = models.Triple.objects.get_or_create(subject=other_sense, predicate=ISOPPOSITEOF, object=sense)
                    context.triples.add(triple)
                    _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
        print 'Added %i negative same-as relations.' % (antonyms_added,)
        
        #TODO:generate links to plural-form
        
        # Create is-a relations.
        isa_added = 0
        #e.g. X=animal Y=[herbivore, omnivore, scavenger, critter, etc] then every Y is-a X
        #e.g. X=dog Y=[puppy, leonberg, working dog, ...] then every Y is-a X
        #[Y for Y in X.hyponyms()] => Y is-a X
        for other_synset in synset.hyponyms()+synset.instance_hyponyms():
            isa_added += 1
            other_word, other_sense = add_word(synset=other_synset, add_relations=False, source=source, context=context, voter=voter)
            if not other_word:
                print 'Skipping'
                continue
            
            triple, _ = models.Triple.objects.get_or_create(subject=other_sense, predicate=ISA, object=sense)
            context.triples.add(triple)
            if _settings.TripleVoteModel and voter:
#                print 'triple:',triple
#                print 'voter:',voter
                _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                
            # Create antonyms.
#            if _settings.TripleVoteModel and voter:
#                for lemma in other_synset.lemmas:
#                    for antonym_lemma in lemma.antonyms():
#                        antonym_synset = antonym_lemma.synset
#                        other_word, other_sense = add_word(synset=antonym_synset, add_relations=False, source=source, context=context, voter=voter)
#                        if not other_word:
#                            continue
#                        triple, _ = models.Triple.objects.get_or_create(context=context, subject=sense, predicate=ISA, object=other_sense)
#                        _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.NO)
        print 'Added %i is-a relations.' % (isa_added,)
        
        # Create has-a relations.
        hasa_added = 0
        for other_synset in synset.member_holonyms()+synset.part_holonyms()+synset.substance_holonyms():
            hasa_added += 1
            other_word, other_sense = add_word(synset=other_synset, add_relations=False, source=source, context=context, voter=voter)
            if not other_word:
                print 'Skipping'
                continue
            
            triple, _ = models.Triple.objects.get_or_create(subject=sense, predicate=ISPARTOF, object=other_sense)
            context.triples.add(triple)
            if _settings.TripleVoteModel and voter:
                _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.YES)
                
            # Create antonyms.
#            if _settings.TripleVoteModel and voter:
#                for lemma in other_synset.lemmas:
#                    for antonym_lemma in lemma.antonyms():
#                        antonym_synset = antonym_lemma.synset
#                        other_word, other_sense = add_word(synset=antonym_synset, add_relations=False, source=source, context=context, voter=voter)
#                        if not other_word:
#                            continue
#                        triple, _ = models.Triple.objects.get_or_create(context=context, subject=sense, predicate=HASA, object=other_sense)
#                        _settings.TripleVoteModel.objects.get_or_create(triple=triple, person=voter, weight=c.NO)
        print 'Added %i has-a relations.' % (hasa_added,)
            
    return word, sense

class Command(BaseCommand):
    help = 'Loads words and senses from WordNet.'
    args = '<words>'
    option_list = BaseCommand.option_list + (
        make_option('--dryrun',
            action='store_true',
            dest='dryrun',
            default=False,
            help='If given, does not commit any changes.'),
        make_option('--context',
            dest='context',
            default='wordnet',
            help='The default context to link all created relations to.'),
        make_option('--max_words',
            dest='max_words',
            default=0,
            help='The maximum number of words to process. Default is all words.'),
        make_option('--i',
            dest='start_i',
            default=0,
            help='The index of the first word to start processing.'),
        )
    
    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        dryrun = options['dryrun']
        start_i = int(options['start_i'])
        target_words = [_.strip().replace('_', ' ') for _ in args]
        
        context = options['context']
        if context.isdigit():
            context = models.Context.objects.get(id=options['context'])
        else:
            context, _ = models.Context.objects.get_or_create(name=options['context'])
        
        settings.DEBUG = False
        django.db.transaction.enter_transaction_management()
        django.db.transaction.managed(True)
        cursor = django.db.connection.cursor()
        voter = _settings.get_default_person
        if voter:
            voter = voter()
        words_processed = 0
        max_words = int(options['max_words'])
        try:
            source, _ = models.Source.objects.get_or_create(name='wordnet')
            commit_freq = 1000
            for pos in 'nvar':#c.WN_POS_TO_LOCAL_POS.iterkeys():
                print '-'*80
                print 'POS:',pos
                #synsets = list(wn.synsets(pos))
                if target_words:
                    synsets = []
                    for _word in target_words:
                        synsets.extend(wn.synsets(_word, pos))
                else:
                    synsets = wn.all_synsets(pos)
                total = 0#len(synsets)
                i = 0
                for synset in synsets:
                    i += 1
                    words_processed += 1
                    
                    if not i % 100:
                        print '\t',synset
                        print '%s - %i of %i' % (pos, i, total)
                        
                    if start_i and words_processed < start_i:
                        continue
                        
                    if not i % commit_freq and not dryrun:
                        print "Committing..."
                        django.db.transaction.commit()
                    
                    new_word, new_sense = add_word(synset, context=context, source=source, voter=voter)
                    if new_word:
                        new_word.save()
                    
                    if max_words and words_processed >= max_words:
                        return
        finally:
            if not dryrun:
                print "Committing..."
                settings.DEBUG = tmp_debug
                django.db.transaction.commit()
                django.db.transaction.leave_transaction_management()
                print "Committed."
            print 'Processed %i words.' % (words_processed,)
            