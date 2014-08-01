# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import uuidfield.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('snotes20', '0003_chatmessage_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='OSFDocumentState',
            fields=[
                ('documentstate_ptr', models.OneToOneField(to='snotes20.DocumentState', auto_created=True, primary_key=True, serialize=False)),
            ],
            options={
            },
            bases=('snotes20.documentstate',),
        ),
        migrations.CreateModel(
            name='OSFNote',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('order', models.IntegerField()),
                ('time', models.PositiveIntegerField(null=True)),
                ('indentation', models.PositiveIntegerField()),
                ('text', models.CharField(max_length=300)),
                ('link', models.URLField(null=True)),
                ('state', models.ForeignKey(to='snotes20.OSFDocumentState')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OSFTag',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='osfnote',
            name='tags',
            field=models.ManyToManyField(to='snotes20.OSFTag'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='osfnote',
            unique_together=set([('order', 'state')]),
        ),
        migrations.AddField(
            model_name='document',
            name='access_time',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentstate',
            name='date',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='documentstate',
            name='id',
            field=uuidfield.fields.UUIDField(unique=True, serialize=False, primary_key=True, blank=True, editable=False, max_length=32),
        ),
    ]
