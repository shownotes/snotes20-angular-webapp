# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0005_document_raw_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='osfnote',
            name='parent',
            field=models.ForeignKey(to='snotes20.OSFNote', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='osfnote',
            name='indentation',
        ),
    ]
