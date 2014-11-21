import logging
import datetime
import time
import timeit

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import snotes20.models as models
import snotes20.contenttypes as contenttypes


logger = logging.getLogger(__name__)


def update_document(doc, sigh):
    prepped = contenttypes.prep_state(doc)

    with transaction.atomic():
        try:
            doc.state.delete()
            doc.raw_state.delete()
        except:
            pass

        raw_state, state = contenttypes.get_state(prepped)

        doc.raw_state = raw_state
        doc.state = state

        raw_state.save()
        state.save()
        doc.save()

        if sigh:
            raw_state, state = contenttypes.get_state(prepped)

            pub = models.Publication()
            pub.raw_state = raw_state
            pub.state = state
            pub.creator = models.NUser.objects.get(pk=1)
            pub.preliminary = True
            pub.create_date = datetime.datetime(2000, 1, 1)
            pub.save()


def update_documents(docs, sigh):
    start_time = datetime.datetime.now()

    for doc in docs:
        logger.debug("Updating document:" + doc.name)
        update_document(doc, sigh)

    duration = datetime.datetime.now() - start_time

    logger.debug("took {}s".format(duration.total_seconds()))


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        mode = 'continuous'

        if len(args) == 1:
            mode = args[0]

        sigh = False

        if mode == 'sighall':
            mode = 'all'
            sigh = True

        if mode == 'continuous':
            while True:
                today = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
                docs = models.Document.objects.all().filter(edit_date__gt=today)
                update_documents(docs, sigh)
                time.sleep(1)
        elif mode == 'all':
            docs = models.Document.objects.all()
            update_documents(docs, sigh)
