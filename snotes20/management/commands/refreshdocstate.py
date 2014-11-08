import logging

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import snotes20.models as models
import snotes20.contenttypes as contenttypes


logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = ''

    def handle(self, *args, **options):
        docs = models.Document.objects.all()

        for doc in docs:
            logger.debug("Document:" + doc.name)

            with transaction.atomic():
                if doc.state:
                    doc.state.delete()
                if doc.raw_state:
                    doc.raw_state.delete()

                raw_state, state = contenttypes.get_state(doc)

                doc.raw_state = raw_state
                doc.state = state

                raw_state.save()
                state.save()
                doc.save()



