# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
import django.utils.timezone
import uuidfield.fields
import datetime
import django.core.validators
import snotes20.models.nuser
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NUser',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(unique=True, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], max_length=30, verbose_name='username')),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='email')),
                ('is_staff', models.BooleanField(default=False, verbose_name='is_staff')),
                ('is_active', models.BooleanField(default=False, verbose_name='is_active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date_joined')),
                ('date_login', models.DateTimeField(null=True, blank=True, verbose_name='date_login')),
                ('color', models.CharField(validators=[django.core.validators.RegexValidator(code='nocolor', message='No color', regex='^[A-F0-9]{6}$')], default=snotes20.models.nuser.get_random_color, max_length=6)),
                ('migrated', models.BooleanField(default=True)),
                ('old_password', models.CharField(null=True, blank=True, default=None, max_length=500)),
                ('bio', models.CharField(blank=True, default='', max_length=400)),
                ('pw_reset_token', models.CharField(null=True, blank=True, max_length=30)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', blank=True, verbose_name='user permissions')),
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
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
                ('order', models.BigIntegerField()),
                ('message', models.CharField(max_length=200)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ChatMessageIssuer',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('access_time', models.DateTimeField(null=True, blank=True)),
                ('creator', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
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
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
                ('shownoters', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='document',
            name='meta',
            field=models.OneToOneField(null=True, blank=True, to='snotes20.DocumentMeta'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='DocumentState',
            fields=[
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='documentmeta',
            name='state',
            field=models.ForeignKey(null=True, blank=True, to='snotes20.DocumentState'),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('source', models.CharField(choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], db_index=True, max_length=100)),
                ('source_id', models.IntegerField(null=True, blank=True, db_index=True, verbose_name='ID at source')),
                ('import_date', models.DateTimeField(null=True, blank=True)),
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
                ('number', models.CharField(null=True, blank=True, max_length=10)),
                ('episode_url', models.URLField(null=True, blank=True, verbose_name='Episode URL')),
                ('date', models.DateTimeField()),
                ('canceled', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('POD', 'Podcast'), ('EVT', 'Event'), ('RAD', 'Radio')], max_length=100)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('stream', models.CharField(null=True, blank=True, max_length=100)),
                ('creator', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
                ('document', models.OneToOneField(on_delete=django.db.models.deletion.SET_NULL, null=True, blank=True, to='snotes20.Document')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterDatasourceLog',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('succeeded', models.BooleanField(default=False)),
                ('error', models.TextField(null=True, blank=True, max_length=1000)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('icon', models.CharField(null=True, blank=True, max_length=10)),
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
            name='OSFDocumentState',
            fields=[
                ('documentstate_ptr', models.OneToOneField(serialize=False, primary_key=True, auto_created=True, to='snotes20.DocumentState')),
            ],
            options={
            },
            bases=('snotes20.documentstate',),
        ),
        migrations.CreateModel(
            name='OSFNote',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('source', models.CharField(choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], db_index=True, max_length=100)),
                ('source_id', models.IntegerField(null=True, blank=True, db_index=True, verbose_name='ID at source')),
                ('import_date', models.DateTimeField(null=True, blank=True)),
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('stream', models.CharField(null=True, blank=True, max_length=100)),
                ('chat', models.CharField(null=True, blank=True, max_length=100)),
                ('type', models.CharField(choices=[('POD', 'Podcast'), ('EVT', 'Event'), ('RAD', 'Radio')], max_length=3)),
                ('deleted', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('creator', models.ForeignKey(null=True, blank=True, to=settings.AUTH_USER_MODEL)),
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
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
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
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
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
                ('id', uuidfield.fields.UUIDField(serialize=False, unique=True, primary_key=True, max_length=32, blank=True, editable=False)),
                ('preliminary', models.BooleanField(default=False)),
                ('comment', models.CharField(max_length=250)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(to='snotes20.Episode')),
                ('podcasters', models.ManyToManyField(to='snotes20.Podcaster')),
                ('publication', models.OneToOneField(null=True, to='snotes20.Publication')),
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
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('meta', models.ForeignKey(to='snotes20.DocumentMeta')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
