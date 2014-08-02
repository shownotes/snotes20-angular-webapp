# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentStateError',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('line', models.PositiveIntegerField()),
                ('message', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextDocumentState',
            fields=[
                ('documentstate_ptr', models.OneToOneField(serialize=False, to='snotes20.DocumentState', primary_key=True, auto_created=True)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=('snotes20.documentstate',),
        ),
    ]
