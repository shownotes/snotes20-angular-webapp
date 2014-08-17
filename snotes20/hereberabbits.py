from django.conf import settings
from django.db.models.signals import post_save

from rest_framework.renderers import JSONRenderer

from uuidfield.fields import StringUUID
from uuid import UUID

import rabbitpy.simple as rbbit

TT_DOCUMENT_NEW = "DOCUMENT_NEW"
TT_DOCUMENT_CHATMESSAGE = "DOCUMENT_CHATMESSAGE"
TT_PUBLICATION_NEW = "PUBLICATION_NEW"
TT_PUBLICATION_REQUESTED = "PUBLICATION_REQUESTED"
TT_EPISODE_NUMBER_CHANGED = "EPISODE_NUMBER_CHANGED"
TT_EPISODE_ADDED = "EPISODE_ADDED"
TT_PODCAST_ADDED = "PODCAST_ADDED"
TT_USER_NEW = "USER_NEW"
TT_USER_UPDATED = "USER_UPDATED"

create_wires = {}


def publish(tt, body, json=False):
    if not settings.RABBITMQ_ENABLED:
        return

    props = {}

    if json:
        props['content_type'] = 'application/json'

    rbbit.publish(uri=settings.RABBITMQ_URI,
                  exchange=tt,
                  body=body,
                  properties=props)


def handle_create(sender, instance, created, **kwargs):
    if not created or sender not in create_wires:
        return

    cfg = create_wires[sender]
    exchange = cfg['tt']

    if cfg['type'] == 'full':
        body = cfg['serializer'](instance).data
    else:
        if isinstance(instance.pk, UUID) or isinstance(instance.pk, StringUUID):
            pk = str(instance.pk)
        else:
            pk = instance.pk

        body = {'pk':pk}

    publish(exchange, JSONRenderer().render(body), json=True)


def add_create_wire(sender, tt, full=False, serializer=None):
    type = 'pk'

    if full and serializer:
        type = 'full'

    create_wires[sender] = {
        'tt': tt,
        'type': type,
        'serializer': serializer
    }


def init():
    if not settings.RABBITMQ_ENABLED:
        return

    post_save.connect(handle_create, dispatch_uid='rbbit')

