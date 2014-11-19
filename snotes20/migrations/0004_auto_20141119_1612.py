# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snotes20.models.nuser
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0003_auto_20141119_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nuser',
            name='color',
            field=models.CharField(default=snotes20.models.nuser.get_random_color, validators=[django.core.validators.RegexValidator(code='nocolor', message='No color', regex='^[A-F0-9]{6}$'), snotes20.models.nuser.validate_user_color], max_length=6),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='osftag',
            name='short',
            field=models.CharField(db_index=True, null=True, unique=True, max_length=20, blank=True),
            preserve_default=True,
        ),
    ]
