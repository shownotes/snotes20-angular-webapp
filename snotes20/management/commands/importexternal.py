import logging
from datetime import datetime, timedelta
import traceback
import sys

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from snotes20.datasources import sources
import snotes20.models as models


logger = logging.getLogger(__name__)


def job_update_podcasts(source):
    logger.info("downloading Podcasts")
    podcasts = source.get_podcasts()

    created = 0
    updated = 0

    logger.info("importing Podcasts")

    with transaction.atomic():
        for podcast, slug in podcasts:
            podqry = models.Podcast.objects.filter(source_id=podcast.source_id).filter(source=source.shortname)

            if podqry.exists():
                dbpod = podqry.get()
                logger.debug("updating {}".format(dbpod))

                # podcast
                podcast.id = dbpod.id
                podcast.save()

                # slug
                slug.podcast = podcast
                if not models.PodcastSlug.objects.filter(slug=slug.slug).exists():
                    slug.save()

                updated += 1
            else:
                logger.debug("creating {}".format(slug))
                podcast.save()
                slug.podcast = podcast
                slug.save()
                created += 1

    return created, 0, 0, updated

def job_update_episodes(source):
    logger.info("downloading Episodes")
    tomorrow = (datetime.today() + timedelta(1))
    episodes = source.get_episodes(datetime.today(), tomorrow)

    created = 0
    skipped = 0
    updated = 0

    logger.info("importing Episodes")
    with transaction.atomic():
        for episode in episodes:
            epqry = models.Episode.objects.filter(source_id=episode.source_id).filter(source=source.shortname)

            if epqry.exists():
                dbep = epqry.get()

                if getattr(dbep, 'document', None) is None:
                    logger.debug("updating {}".format(dbep))
                    episode.id = dbep.id
                    episode.save()
                    updated += 1
                else:
                    logger.debug("skipped {}".format(dbep))
                    skipped += 1
            else:
                logger.debug("creating {}".format(episode))
                created += 1
                episode.save()

    return created, 0, skipped, updated

def job_delete_deleted_episodes(source):
    yesterday = (datetime.today() - timedelta(1))
    src_deleted = source.get_deleted_episodes(yesterday)
    qry = models.Episode.objects.filter(source_id__in=src_deleted)
    deleted = qry.count()
    logger.info("%i Episodes", deleted)
    qry.delete()

    return 0, deleted, 0, 0

def job_delete_old_episodes(source):
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    qry = models.Episode.objects.filter(date__lt=today).filter(document=None)
    deleted = qry.count()
    logger.info("%i Episodes", deleted)
    qry.delete()

    return 0, deleted, 0, 0

jobs = []

def add_job(job):
    name = job.__name__[3:].replace('_', ' ')
    jobs.append((name, job))

add_job(job_update_podcasts)
add_job(job_update_episodes)
add_job(job_delete_deleted_episodes)
add_job(job_delete_old_episodes)


def import_from_source(source):
    srcLog = models.ImporterDatasourceLog()
    jobLogs = []

    srcLog.start()

    for name, job in jobs:
        jobLog = models.ImporterJobLog()
        jobLog.name = name

        jobLog.start()

        try:
            jobLog.created,\
                jobLog.deleted,\
                jobLog.skipped,\
                jobLog.updated = job(source)

            jobLog.succeeded = True
        except Exception:
            jobLog.succeeded = False

            exc_type, exc_value, exc_traceback = sys.exc_info()
            jobLog.error = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

        jobLog.stop()
        jobLogs.append(jobLog)

    srcLog.stop()

    return srcLog, jobLogs


class Command(BaseCommand):
    args = ''
    help = 'Updates all external datasources'

    def handle(self, *args, **options):
        log = models.ImporterLog()
        srcLogs = []

        log.start()

        logger.info("importing from external sources")
        for source in sources:
            logger.info("import from {}".format(source.name))
            srcLog = import_from_source(source)
            srcLog[0].source = source.shortname
            srcLogs.append(srcLog)

        log.stop()

        log.save()

        for srcLog, jobLogs in srcLogs:
            srcLog.log = log
            srcLog.save()

            for jobLog in jobLogs:
                jobLog.source = srcLog
                jobLog.save()
