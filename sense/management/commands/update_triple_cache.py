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
    help = 'Updates triple cache.'
    args = ''
    option_list = BaseCommand.option_list + (
        make_option('--dryrun',
            action='store_true',
            dest='dryrun',
            default=False,
            help='If given, does not commit any changes.'),
        make_option('--context',
            dest='context',
            default='global',
            help='The name of the context to update.'),
        )
    
    def handle(self, *args, **options):
        
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        
        context = models.Context.objects.get(name=options['context'])
        context.refresh_triple_cache(save=True, clear=False, force=True)
        