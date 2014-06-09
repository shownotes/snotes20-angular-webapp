from django.core.management.base import BaseCommand, CommandError
import logging
import datetime

from snotes20.datasources import sources
import snotes20.models as models

logger = logging.getLogger(__name__)


def import_from_source(source):
    logger.info("importing Podcasts")
    podcasts = source.get_podcasts()
    import_thing(source, podcasts, models.Podcast.objects)

    logger.info("importing Episodes")
    yesterday = (datetime.date.today() - datetime.timedelta(1))
    tomorrow = (datetime.date.today() + datetime.timedelta(1))
    episodes = source.get_episodes(yesterday, tomorrow)
    import_thing(source, episodes, models.Episode.objects.filter(document=None))


def import_thing(source, data, oqry):
    for entry in data:
        qry = oqry.filter(source_id=entry.source_id).filter(source=source.shortname)

        if qry.exists():
            dbentry = qry.get()
            logger.debug("updating {}".format(dbentry))
        else:
            logger.debug("creating {}".format(entry))
            entry.save()


class Command(BaseCommand):
    args = ''
    help = 'Updates all external datasources'

    def handle(self, *args, **options):
        logger.info("importing from external sources")
        for source in sources:
            logger.info("import from {}".format(source.name))
            import_from_source(source)
