# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
import datetime
import django.utils.timezone
import snotes20.models.nuser
from django.conf import settings
import uuidfield.fields
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='NUser',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('password', models.CharField(verbose_name='password', max_length=128)),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status', default=False)),
                ('username', models.CharField(unique=True, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30)),
                ('email', models.EmailField(unique=True, verbose_name='email', max_length=75)),
                ('is_staff', models.BooleanField(verbose_name='is_staff', default=False)),
                ('is_active', models.BooleanField(verbose_name='is_active', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date_joined', default=django.utils.timezone.now)),
                ('date_login', models.DateTimeField(blank=True, verbose_name='date_login', null=True)),
                ('color', models.CharField(validators=[django.core.validators.RegexValidator(message='No color', code='nocolor', regex='^[A-F0-9]{6}$')], default=snotes20.models.nuser.get_random_color, max_length=6)),
                ('migrated', models.BooleanField(default=True)),
                ('old_password', models.CharField(blank=True, null=True, default=None, max_length=500)),
                ('bio', models.CharField(blank=True, default='', max_length=400)),
                ('pw_reset_token', models.CharField(blank=True, null=True, max_length=30)),
                ('groups', models.ManyToManyField(blank=True, to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChatMessage',
            fields=[
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('message', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChatMessageIssuer',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('type', models.CharField(choices=[('USR', 'User')], max_length=3)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='issuer',
            field=models.OneToOneField(to='snotes20.ChatMessageIssuer'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('name', models.CharField(serialize=False, primary_key=True, max_length=40)),
                ('editor', models.CharField(choices=[('EP', 'Etherpad')], max_length=3)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('type', models.CharField(choices=[('OSF', 'OSF'), ('TXT', 'Text')], max_length=3)),
                ('creator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='document',
            field=models.ForeignKey(to='snotes20.Document'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DocumentMeta',
            fields=[
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('shownoters', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='document',
            name='meta',
            field=models.OneToOneField(blank=True, to='snotes20.DocumentMeta', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DocumentState',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='documentmeta',
            name='state',
            field=models.ForeignKey(blank=True, to='snotes20.DocumentState', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('source', models.CharField(choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], db_index=True, max_length=100)),
                ('source_id', models.IntegerField(blank=True, db_index=True, verbose_name='ID at source', null=True)),
                ('import_date', models.DateTimeField(blank=True, null=True)),
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('number', models.CharField(blank=True, null=True, max_length=10)),
                ('episode_url', models.URLField(blank=True, verbose_name='Episode URL', null=True)),
                ('date', models.DateTimeField()),
                ('canceled', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('POD', 'Podcast'), ('EVT', 'Event'), ('RAD', 'Radio')], max_length=100)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('stream', models.CharField(blank=True, null=True, max_length=100)),
                ('creator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('document', models.OneToOneField(blank=True, on_delete=django.db.models.deletion.SET_NULL, to='snotes20.Document', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterDatasourceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('source', models.CharField(choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], max_length=3)),
            ],
            options={
                'verbose_name': 'Importer source log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterJobLog',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('succeeded', models.BooleanField(default=False)),
                ('error', models.TextField(blank=True, null=True, max_length=1000)),
                ('created', models.PositiveIntegerField(default=0)),
                ('deleted', models.PositiveIntegerField(default=0)),
                ('skipped', models.PositiveIntegerField(default=0)),
                ('updated', models.PositiveIntegerField(default=0)),
                ('source', models.ForeignKey(to='snotes20.ImporterDatasourceLog')),
            ],
            options={
                'verbose_name': 'Importer job log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterLog',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Importer run log',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='importerdatasourcelog',
            name='log',
            field=models.ForeignKey(to='snotes20.ImporterLog'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='NUserEmailToken',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('token', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Email token',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUserSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('value', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Social',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUserSocialType',
            fields=[
                ('name', models.SlugField(serialize=False, primary_key=True)),
                ('human_name', models.CharField(max_length=20)),
                ('icon', models.CharField(blank=True, null=True, max_length=10)),
            ],
            options={
                'verbose_name': 'Social Type',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='nusersocial',
            name='type',
            field=models.ForeignKey(to='snotes20.NUserSocialType'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='nusersocial',
            unique_together=set([('user', 'type')]),
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('source', models.CharField(choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], db_index=True, max_length=100)),
                ('source_id', models.IntegerField(blank=True, db_index=True, verbose_name='ID at source', null=True)),
                ('import_date', models.DateTimeField(blank=True, null=True)),
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('stream', models.CharField(blank=True, null=True, max_length=100)),
                ('chat', models.CharField(blank=True, null=True, max_length=100)),
                ('type', models.CharField(choices=[('POD', 'Podcast'), ('EVT', 'Event'), ('RAD', 'Radio')], max_length=3)),
                ('deleted', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('creator', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='episode',
            name='podcast',
            field=models.ForeignKey(to='snotes20.Podcast'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Podcaster',
            fields=[
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('uri', models.URLField(unique=True, db_index=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PodcastSlug',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.SlugField(unique=True)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('podcast', models.ForeignKey(to='snotes20.Podcast')),
            ],
            options={
                'get_latest_by': 'date_added',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('create_date', models.DateTimeField()),
                ('preliminary', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=250)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(to='snotes20.Episode')),
                ('podcasters', models.ManyToManyField(to='snotes20.Podcaster')),
                ('shownoters', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(to='snotes20.DocumentState')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationRequest',
            fields=[
                ('id', uuidfield.fields.UUIDField(editable=False, unique=True, serialize=False, primary_key=True, max_length=32, blank=True)),
                ('preliminary', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=250)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(to='snotes20.Episode')),
                ('podcasters', models.ManyToManyField(to='snotes20.Podcaster')),
                ('publication', models.OneToOneField(to='snotes20.Publication', null=True)),
                ('requester', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('shownoters', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('state', models.ForeignKey(to='snotes20.DocumentState')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawPodcaster',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('meta', models.ForeignKey(to='snotes20.DocumentMeta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
