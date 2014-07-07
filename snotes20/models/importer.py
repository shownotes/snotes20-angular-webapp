from datetime import datetime, timedelta

from django.db import models

from snotes20.models import SOURCE_CHOICES


class Timeable(models.Model):
    starttime = models.DateTimeField()
    endtime = models.DateTimeField()

    def start(self):
        self.starttime = datetime.now()

    def stop(self):
        self.endtime = datetime.now()

    @property
    def runtime(self):
        if self.starttime is None or self.endtime is None:
            return timedelta()
        else:
            return self.endtime - self.starttime

    class Meta:
        abstract = True
        verbose_name = "Importer run log"


class ImporterLog(Timeable):

    @property
    def succeeded(self):
        return all(src.succeeded for src in self.sources.all())

    @property
    def created(self):
        return sum(src.created for src in self.sources)

    @property
    def deleted(self):
        return sum(src.deleted for src in self.sources)

    @property
    def skipped(self):
        return sum(src.skipped for src in self.sources)

    @property
    def updated(self):
        return sum(src.updated for src in self.sources)

    def __str__(self):
        return self.starttime.strftime('%G-%m-%d %T')


class ImporterDatasourceLog(Timeable):
    log = models.ForeignKey(ImporterLog, related_name="sources")

    source = models.CharField(max_length=3, choices=SOURCE_CHOICES)

    @property
    def succeeded(self):
        return all(job.succeeded for job in self.jobs.all())

    @property
    def created(self):
        return sum(job.created for job in self.jobs)

    @property
    def deleted(self):
        return sum(job.deleted for job in self.jobs)

    @property
    def skipped(self):
        return sum(job.skipped for job in self.jobs)

    @property
    def updated(self):
        return sum(job.updated for job in self.jobs)

    class Meta:
        verbose_name = "Importer source log"

    def __str__(self):
        rtn = self.starttime.strftime('%G-%m-%d %T')
        if not self.succeeded:
            rtn += " (not succeeded)"
        else:
            rtn += " (succeeded)"
        return rtn


class ImporterJobLog(Timeable):
    source = models.ForeignKey(ImporterDatasourceLog, related_name="jobs")
    name = models.CharField(max_length=30)

    succeeded = models.BooleanField(default=False)
    error = models.TextField(max_length=1000, null=True, blank=True)

    created = models.PositiveIntegerField(default=0)
    deleted = models.PositiveIntegerField(default=0)
    skipped = models.PositiveIntegerField(default=0)
    updated = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Importer job log"
