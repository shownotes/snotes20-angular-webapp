# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0004_auto_20140802_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='raw_state',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='snotes20.TextDocumentState', blank=True),
            preserve_default=True,
        ),
    ]
