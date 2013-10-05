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
        )
    
    def handle(self, *args, **options):
        tmp_debug = settings.DEBUG
        settings.DEBUG = False
        django.db.transaction.enter_transaction_management()
        django.db.transaction.managed(True)
        try:
            q = models.PredicateObjectIndex.objects.filter(check_enabled=True)
            q = q.order_by('-depth')
            total = q.count()
            print 'Total:', total
            i = 0
            for r in q.iterator():
                i += 1
                print '%i of %i' % (i, total)
                r.propagate_enabled(auto_commit=True)
        finally:
            print "Committing..."
            settings.DEBUG = tmp_debug
            django.db.transaction.commit()
            django.db.transaction.leave_transaction_management()
            print "Committed."