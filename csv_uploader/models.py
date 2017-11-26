# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models
from djutil.models import TimeStampedModel


class CsvJob(TimeStampedModel):

    SuccessStatus = 'success'
    FailedStatus = 'failed'
    PendingStatus = 'pending'

    STATUSES = (
        (SuccessStatus, 'success'),
        (FailedStatus, 'failed'),
        (PendingStatus, 'pending')
    )

    action_name = models.CharField(max_length=20)
    status = models.CharField(choices=STATUSES, max_length=20)
    uploaded_by = models.ForeignKey(User)

    def resync_status(self):
        if self.item_count(CsvJobItem.FailedStatus)==0 and self.item_count(CsvJobItem.PendingStatus)==0:
            self.status = 'success'
            self.save()

    def item_count(self, status):
            return CsvJobItem.objects.filter(csv_job=self, status=status).count()

    @classmethod
    def purge(cls, days=2):
        CsvJob.objects.filter(created_at__lt=(datetime.now() - timedelta(days=days))).delete()

class CsvJobItem(models.Model):

    SuccessStatus = 'success'
    FailedStatus = 'failed'
    PendingStatus = 'pending'

    STATUSES = (
        (SuccessStatus, 'success'),
        (FailedStatus, 'failed'),
        (PendingStatus, 'pending')
    )

    csv_job = models.ForeignKey(CsvJob, related_name="csv_jobs")
    row_values = models.TextField()
    status = models.CharField(choices=STATUSES, max_length=20)
    message = models.CharField(max_length=200, null=True)

