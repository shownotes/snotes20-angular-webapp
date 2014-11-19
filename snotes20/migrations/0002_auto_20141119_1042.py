# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osftag',
            name='name',
            field=models.CharField(max_length=50, unique=True, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='osftag',
            name='short',
            field=models.CharField(max_length=20, unique=True, db_index=True),
            preserve_default=True,
        ),
    ]
