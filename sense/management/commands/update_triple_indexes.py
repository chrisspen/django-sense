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
from django.db.models import F, Q
import django
from django.utils.encoding import smart_text, smart_unicode

from sense import models
from sense import constants as c
from sense import settings as _settings

class Command(BaseCommand):
    help = 'Updates triple indexes.'
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('--dryrun',
            action='store_true',
            dest='dryrun',
            default=False,
            help='If given, does not commit any changes.'),
        make_option('--predicate',
            dest='predicate',
            default=None,
            help='The predicate to filter generation by.'),
        make_option('--subject',
            dest='subject',
            default=None,
            help='The subject to start at.'),
        make_option('--object',
            dest='object',
            default=None,
            help='The object to start at.'),
        make_option('--depth',
            dest='depth',
            default=0,
            help='The starting depth.'),
        make_option('--noseed',
            action='store_true',
            dest='noseed',
            default=False,
            help='If given, does seed any index records.'),
        make_option('--noupdate',
            action='store_true',
            dest='noupdate',
            default=False,
            help='If given, does update any index records.'),
        )
    
    def handle(self, *args, **options):
        dryrun = options['dryrun']
        subject = options['subject']
        predicate = options['predicate']
        object = options['object']
        depth = int(options['depth'])
        
        voter = _settings.get_default_person
        if voter:
            voter = voter()
        
        settings.DEBUG = False
#        django.db.transaction.enter_transaction_management()
#        django.db.transaction.managed(True)
        
#        if not options['noseed']:
#            models.PredicateObjectIndexPending.populate(predicate=predicate)
#        
#        if not options['noupdate']:
#            models.PredicateObjectIndex.update_all(predicate=predicate, depth=depth)
#        
        models.PredicateObjectIndex.update_all_best()
        