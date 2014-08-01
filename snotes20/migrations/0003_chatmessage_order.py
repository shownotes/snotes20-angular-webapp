# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0002_chatmessage_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='order',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
