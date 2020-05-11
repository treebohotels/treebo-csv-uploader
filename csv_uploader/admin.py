# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import CsvJob,CsvJobItem


@admin.register(CsvJob)
class CsvJobAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'action_name', 'status', 'uploaded_by')


@admin.register(CsvJobItem)
class CsvJobItemAdmin(admin.ModelAdmin):
    list_display = ('csv_job', 'row_values', 'status', 'message')
