===================
treebo-csv-uploader
===================


This project provides a generic user interface for uploading csv files and registering actions for uploaded values...

Installation
------------

First add to requirement file:

.. code::

    treebo-csv-uploader

Add urls:

.. code:: python

    urlpatterns = [
        # ...
        url(r'^csv/$', include('csv_uploader.urls')),
    ]

Add the ``treebo-csv-uploader`` applications to your ``INSTALLED_APPS``:

.. code:: python

    INSTALLED_APPS += [
        # ...
        'treebo_csv_uploader.apps.CsvUploaderConfig',                             # required
    ]

SAMPLE CONFIGURATION:

.. code:: python

    CSV_UPLOADER = [{"actions": {
                                    "<action1>": {
                                        "base_path": '<path.of.validators>'
                                },
                                    "action1": {
                                        "base_path": 'path.of.validators'
                                    }
                                }
                    }]

at base path register validators and handlers:
handlers.py:

.. code:: python

    from integrations.notifications.async_service import AsyncNotificationService
    from csv_uploader.handler import CsvHandlerRegisty


    @CsvHandlerRegisty.async_handler('INVOICE_MAILER')
    def handle_invoice_mailer(invoice, job_id):
     AsyncNotificationService.mail_invoices([invoice['INVOICE_ID']], job_id)
     return True

validators.py:

.. code:: python

    from csv_uploader.validator import CsvValidatorRegistry


    @CsvValidatorRegistry.header_validator('INVOICE_MAILER', ['INVOICE_ID'])    
    def validate_invoice_mailer_header(user, header):
     return header==['INVOICE_ID']


    @CsvValidatorRegistry.row_validator('INVOICE_MAILER')
    def validate_invoice_mailer_row(user, args):
        return True
