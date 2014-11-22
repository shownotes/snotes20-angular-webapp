# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0004_auto_20141119_1612'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osfnote',
            name='url',
            field=models.URLField(max_length=1500, null=True),
            preserve_default=True,
        ),
    ]
