# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
import logging
import csv

from models import CsvJobItem, CsvJob
from validator import CsvValidator

class CsvHandler:

    def __init__(self, action_name, file):
        for action, conf in settings.CSV_UPLOADER[0]['actions'].items():
            __import__(conf['base_path'])
        self.action, self.file = action_name, file
        self.statuses = []
        self.job = None
        self.handler = CsvHandlerRegisty.HANDLERS[action_name]
        self.validator = CsvValidator(action_name)

    def process(self, current_user):
        reader = csv.DictReader(self.file)
        if not self.validator.validate_header(current_user, reader.fieldnames):
            raise Exception("Invalid header")

        self.job = CsvJob(action_name=self.action, status='pending', uploaded_by=current_user)
        self.job.save()
        for row in reader:
            if not self.validator.csv_row_validator(current_user, row):
                CsvJobItem(status='failed', row_values=str(row), csv_job=self.job).save()
            else:
                self.handle(row)
        self.job.resync_status()


    def handle(self, args):
        logger = logging.getLogger(self.__class__.__name__)
        job_item = CsvJobItem(status='pending', row_values = str(args), csv_job= self.job)
        job_item.save()
        try:
            self.handler['action'](args, job_item.id)
            if self.handler['async']:
                job_item.status = 'pending'
            else:
                job_item.status = 'success'
        except Exception as e:
            logger.error(e)
            job_item.status = 'failed'
        job_item.save()

    def display_message(self):
        return "Success: "+ str(self.job.item_count('success')) + "  Pending " + str(self.job.item_count('pending'))


    @classmethod
    def callback(cls, job_item_id, status, message):
        """
        :param job_id: csv_action to be registered as synchronous
        :param status: decorated function
        :message: detailed message if applicable
        """
        job_item = CsvJobItem.objects.get(id=job_item_id)
        job_item.status = status
        job_item.message = message
        job_item.save()
        job_item.csv_job.resync_status()


class CsvHandlerRegisty:

    HANDLERS={}

    @classmethod
    def sync_handler(cls, action_name):
        """
        :param action_name: csv_action to be registered as synchronous
        :param handler_func: decorated function
        :return: none
        """
        def decorator(handler_function):
            cls.HANDLERS[action_name] = dict(action=handler_function, async=False)

            def register_csv_handler(*args):
                return register_csv_handler
        return decorator

    @classmethod
    def async_handler(cls, action_name):
        """
        :param action_name: csv_action to be registered as asynchronous
        :param handler_func: decorated function
        :return: none
        """
        def decorator(handler_function):
            cls.HANDLERS[action_name] = dict(action=handler_function, async=True)
            def register_csv_handler(*args):
                return register_csv_handler
        return decorator
