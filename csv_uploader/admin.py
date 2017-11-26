# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from models import CsvJob,CsvJobItem
# Register your models here.
admin.site.register(CsvJob)
admin.site.register(CsvJobItem)