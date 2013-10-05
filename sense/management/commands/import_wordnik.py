#!/usr/bin/python
import datetime
import os
import random
import re
import sys
import time
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core import serializers
import django

from sense import models
from sense import constants
from sense import utils

#NOTE:experimental
class Command(BaseCommand):
    help = 'Import definitions from Wordnik.'
    args = ''
    option_list = BaseCommand.option_list #+ (
#        make_option('--format',
#            dest='format',
#            default='json',),
#        make_option('--indent',
#            dest='indent',
#            default=4,),
#        )
    
    def handle(self, *args, **options):
        
        from wordnik import swagger, WordApi
        client = swagger.ApiClient(settings.WORDNIK_KEY, settings.WORDNIK_API)
        wordApi = WordApi.WordApi(client)
        definitions = wordApi.getDefinitions('child',
                                     partOfSpeech='noun',
                                     #sourceDictionaries='wiktionary',
                                     limit=1)
        for definition in definitions:
            print definition.text
        
        return
        total = len(args)
        word_i = 0
        invalid_pos_names = set()
        skip_to = 0
        for word_text in args:
            word_i += 1
            if word_i < skip_to:
                continue
            print '='*80
            print '%s (%i of %i)' % (word_text, word_i, total)
            
            utils.import_from_wordnik(
                word_text,
                invalid_pos_names=invalid_pos_names)
            
            #break
            dsecs = random.randint(1,5)
            print 'Waiting for %i seconds...' % (dsecs,)
            time.sleep(dsecs)
        print '='*80
        print 'Invalid part-of-speech names:',sorted(invalid_pos_names)
        