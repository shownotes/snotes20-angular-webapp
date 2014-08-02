# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0003_auto_20140802_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentstateerror',
            name='state',
            field=models.ForeignKey(to='snotes20.DocumentState', default=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='document',
            name='type',
            field=models.CharField(choices=[('OSF', 'OSF'), ('TXT', 'Text')], max_length=3, default='OSF'),
        ),
    ]
