# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

import json

class CsvValidator:


    def __init__(self, action_name):
        action_name = action_name
        self.csv_row_validator = CsvValidatorRegistry.ROW_VALIDATORS[action_name]
        self.csv_header_validator = CsvValidatorRegistry.HEADER_VALIDATORS[action_name]['action']

    def validate_header(self, user, header):
        return self.csv_header_validator(user, header)

    def validate_row(self, user, row):
        return self.csv_row_validator(user, row)

    @classmethod
    def available_actions(cls):
        cls.import_validators()
        return CsvValidatorRegistry.HEADER_VALIDATORS

    @classmethod
    def import_validators(cls):
        for action, conf in settings.CSV_UPLOADER[0]['actions'].items():
            __import__(conf['base_path'])

    @classmethod
    def available_actions_json(cls):
        data = {}
        for action, detail in CsvValidatorRegistry.HEADER_VALIDATORS.items():
            data[action] = detail['header']
        return json.dumps(data)


class CsvValidatorRegistry:

    ROW_VALIDATORS = {}
    HEADER_VALIDATORS = {}

    @classmethod
    def header_validator(cls, action_name, header):
        """
        :param action_name: csv_action to be registered as asynchronous
        :param handler_func: decorated function
        :return: none
        """
        def decorator(handler_function):
            cls.HEADER_VALIDATORS[action_name] = dict(action=handler_function
                                                               , header=header)
            def register_csv_validator(arg):
                return handler_function
        return decorator

    @classmethod
    def row_validator(cls, action_name):
        """
        :param action_name: csv_action to be registered as asynchronous
        :param handler_func: decorated function
        :return: none
        """
        def decorator(handler_function):
            cls.ROW_VALIDATORS[action_name] = handler_function
            def register_csv_validator(*args):
                return handler_function
        return decorator
