# -*- coding: utf-8 -*-

from django.conf.urls import url, include

from views import CsvUploader, CsvUploaderCallback, CsvUploaderCleanup

urlpatterns = [

    url(r'^upload/$', CsvUploader.as_view(), name='upload-csv', ),
    url(r'^callback/$', CsvUploaderCallback.as_view(), name='upload-csv-callback', ),
    url(r'^cleanup/$', CsvUploaderCleanup.as_view(), name='upload-csv-cleanup', )

]
