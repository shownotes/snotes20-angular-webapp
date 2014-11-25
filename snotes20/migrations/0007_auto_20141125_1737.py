# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0006_podcast_feed'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='episode',
            unique_together=set([('podcast', 'number')]),
        ),
    ]
