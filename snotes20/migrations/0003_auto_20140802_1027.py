# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0002_documentstateerror_textdocumentstate'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='snotes20.DocumentState', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='documentmeta',
            name='state',
        ),
    ]
