# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0005_auto_20141122_0011'),
    ]

    operations = [
        migrations.AddField(
            model_name='podcast',
            name='feed',
            field=models.URLField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
