# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

from django.db import models
from django.conf import settings

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
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL)

    def resync_status(self):
        if self.item_count(CsvJobItem.FailedStatus)==0 and self.item_count(CsvJobItem.PendingStatus)==0:
            self.status = self.SuccessStatus
        elif self.item_count(CsvJobItem.PendingStatus)==0:
            self.status = self.FailedStatus
        else:
            self.status = self.PendingStatus
        self.save()

    def item_count(self, status):
            return CsvJobItem.objects.filter(csv_job=self, status=status).count()

    def __str__(self):
        return str(self.created_at)

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

