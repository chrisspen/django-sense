#!/usr/bin/python
import datetime
import os
import re
import sys
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core import serializers
import django

from sense import models

class Command(BaseCommand):
    help = 'Dumps words, and all related models, to JSON incrementally.'
    args = '<words>'
    option_list = BaseCommand.option_list + (
        make_option('--format',
            dest='format',
            default='json',),
        make_option('--indent',
            dest='indent',
            default=4,),
        )
    
    def handle(self, *args, **options):
        print 'args:',args
        serializer = serializers.get_serializer(options['format'])()
        print '[',
        indent = int(options['indent'])
        priors = set()
        first = True
        for word_text in args:
            word_text = word_text.replace('_', ' ')
            
            # Collect objects to serialize.
            try:
                word = models.Word.objects.get(text=word_text)
            except models.Word.DoesNotExist:
                print>>sys.stderr, 'Word "%s" does not exist.' % (word_text,)
                continue
            if word in priors:
                continue
            objs = []
            objs.append(word)
            priors.add(word)
            for sense in word.senses.all():
                if sense.source not in priors:
                    if sense.source:
                        objs.append(sense.source)
                    priors.add(sense.source)
                for example in sense.examples.all():
                    if example not in priors:
                        objs.append(example)
                        priors.add(example)
                objs.append(sense)
            
            # Generate serialized data.
            data = serializer.serialize(
                objs,
                use_natural_keys=True,
                indent=indent,
            )[1:-1].rstrip()
            
            # Remove literal primary key.
            data = re.sub('"pk"\:\s+[0-9]+,', '"pk": null,', data)[:-1]
            
            if first:
                first = False
            else:
                data = (','+data)
            print data
        print ']',
        