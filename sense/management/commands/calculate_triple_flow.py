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
    help = 'Generate triple flow records for displaying triples in a logically consistent order.'
    args = '<context ids>'
    option_list = BaseCommand.option_list + (
    )
    
    def handle(self, *args, **options):
        q = models.Context.objects.filter(id__in=map(int, args))
        for context in q.iterator():
            models.TripleFlow.calculate_flow(context)
            