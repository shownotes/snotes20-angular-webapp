import logging
import datetime

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from snotes20.datasources import sources
import snotes20.models as models


logger = logging.getLogger(__name__)


def import_from_source(source):
    logger.info("downloading Podcasts")
    podcasts = source.get_podcasts()

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
            else:
                logger.debug("creating {}".format(slug))
                podcast.save()
                slug.podcast = podcast
                slug.save()

    logger.info("downloading Episodes")
    tomorrow = (datetime.date.today() + datetime.timedelta(1))
    episodes = source.get_episodes(datetime.date.today(), tomorrow)

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
                else:
                    logger.debug("skipped {}".format(dbep))
            else:
                logger.debug("creating {}".format(episode))
                episode.save()

    logger.info("deleting old Episodes")
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    qry = models.Episode.objects.filter(date__lt=today).filter(document=None)
    logger.info("%i Episodes", qry.count())
    qry.delete()

class Command(BaseCommand):
    args = ''
    help = 'Updates all external datasources'

    def handle(self, *args, **options):
        logger.info("importing from external sources")
        for source in sources:
            logger.info("import from {}".format(source.name))
            import_from_source(source)
