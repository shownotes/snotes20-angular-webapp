# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0002_auto_20141119_1042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osfnote',
            name='state',
            field=models.ForeignKey(related_name='shownotes', null=True, blank=True, to='snotes20.OSFDocumentState'),
            preserve_default=True,
        ),
    ]
