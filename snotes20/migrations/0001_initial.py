# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import snotes20.models.cover
import django_extensions.db.fields
import datetime
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
import snotes20.models.nuser


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(verbose_name='last login', default=django.utils.timezone.now)),
                ('is_superuser', models.BooleanField(verbose_name='superuser status', help_text='Designates that this user has all permissions without explicitly assigning them.', default=False)),
                ('username', models.CharField(max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')], unique=True)),
                ('email', models.EmailField(max_length=75, verbose_name='email', unique=True)),
                ('is_staff', models.BooleanField(verbose_name='is_staff', default=False)),
                ('is_active', models.BooleanField(verbose_name='is_active', default=False)),
                ('date_joined', models.DateTimeField(verbose_name='date_joined', default=django.utils.timezone.now)),
                ('date_login', models.DateTimeField(blank=True, verbose_name='date_login', null=True)),
                ('color', models.CharField(max_length=6, validators=[django.core.validators.RegexValidator(code='nocolor', regex='^[A-F0-9]{6}$', message='No color')], default=snotes20.models.nuser.get_random_color)),
                ('migrated', models.BooleanField(default=True)),
                ('old_password', models.CharField(max_length=500, blank=True, default=None, null=True)),
                ('bio', models.CharField(max_length=400, blank=True, default='')),
                ('pw_reset_token', models.CharField(max_length=30, blank=True, null=True)),
                ('groups', models.ManyToManyField(to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', related_name='user_set', verbose_name='groups', related_query_name='user')),
                ('user_permissions', models.ManyToManyField(to='auth.Permission', blank=True, help_text='Specific permissions for this user.', related_name='user_set', verbose_name='user permissions', related_query_name='user')),
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
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
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
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('type', models.CharField(max_length=3, choices=[('USR', 'User')])),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cover',
            fields=[
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('file', models.ImageField(upload_to=snotes20.models.cover.f)),
                ('original_url', models.URLField()),
                ('create_date', models.DateTimeField()),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Document',
            fields=[
                ('name', models.CharField(max_length=40, primary_key=True, serialize=False)),
                ('editor', models.CharField(max_length=3, choices=[('EP', 'Etherpad')])),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('access_date', models.DateTimeField(blank=True, null=True)),
                ('edit_date', models.DateTimeField(blank=True, null=True)),
                ('type', models.CharField(max_length=3, choices=[('OSF', 'OSF'), ('TXT', 'Text')], default='OSF')),
                ('access_time', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentMeta',
            fields=[
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentState',
            fields=[
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('date', models.DateTimeField(default=datetime.datetime.now)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DocumentStateError',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('line', models.PositiveIntegerField()),
                ('message', models.CharField(max_length=400)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Episode',
            fields=[
                ('source', models.CharField(max_length=100, db_index=True, choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], default='INT')),
                ('source_id', models.IntegerField(verbose_name='ID at source', blank=True, db_index=True, null=True)),
                ('import_date', models.DateTimeField(blank=True, null=True)),
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('title', models.CharField(max_length=200, blank=True, null=True)),
                ('number', models.CharField(max_length=10, blank=True, null=True)),
                ('episode_url', models.URLField(blank=True, verbose_name='Episode URL', null=True)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('canceled', models.BooleanField(default=False)),
                ('type', models.CharField(max_length=100, choices=[('POD', 'Podcast'), ('EVT', 'Event'), ('RAD', 'Radio')])),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('stream', models.CharField(max_length=100, blank=True, null=True)),
                ('cover', models.ForeignKey(to='snotes20.Cover', blank=True, related_name='episodes', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('document', models.OneToOneField(to='snotes20.Document', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True)),
            ],
            options={
                'permissions': (('publish_episode', 'publish'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterDatasourceLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('source', models.CharField(max_length=3, choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')])),
            ],
            options={
                'verbose_name': 'Importer source log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterJobLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
                ('name', models.CharField(max_length=30)),
                ('succeeded', models.BooleanField(default=False)),
                ('error', models.TextField(max_length=1000, blank=True, null=True)),
                ('created', models.PositiveIntegerField(default=0)),
                ('deleted', models.PositiveIntegerField(default=0)),
                ('skipped', models.PositiveIntegerField(default=0)),
                ('updated', models.PositiveIntegerField(default=0)),
                ('source', models.ForeignKey(to='snotes20.ImporterDatasourceLog', related_name='jobs')),
            ],
            options={
                'verbose_name': 'Importer job log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ImporterLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('starttime', models.DateTimeField()),
                ('endtime', models.DateTimeField()),
            ],
            options={
                'abstract': False,
                'verbose_name': 'Importer run log',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUserEmailToken',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('email', models.EmailField(max_length=75, unique=True)),
                ('token', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='email_tokens')),
            ],
            options={
                'verbose_name': 'Email token',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUserSocial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('value', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': 'Social',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NUserSocialType',
            fields=[
                ('name', models.SlugField(primary_key=True, serialize=False)),
                ('human_name', models.CharField(max_length=20)),
                ('icon', models.CharField(max_length=10, blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Social Type',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OSFDocumentState',
            fields=[
                ('documentstate_ptr', models.OneToOneField(to='snotes20.DocumentState', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
            ],
            options={
            },
            bases=('snotes20.documentstate',),
        ),
        migrations.CreateModel(
            name='OSFNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('order', models.IntegerField()),
                ('timestamp', models.BigIntegerField(null=True)),
                ('title', models.TextField()),
                ('url', models.URLField(null=True)),
                ('parent', models.ForeignKey(to='snotes20.OSFNote', blank=True, related_name='shownotes', null=True)),
                ('state', models.ForeignKey(to='snotes20.OSFDocumentState', related_name='shownotes')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OSFTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('short', models.CharField(max_length=20)),
                ('description', models.CharField(max_length=200)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Podcast',
            fields=[
                ('source', models.CharField(max_length=100, db_index=True, choices=[('INT', 'Internal'), ('HOE', 'Hoersuppe')], default='INT')),
                ('source_id', models.IntegerField(verbose_name='ID at source', blank=True, db_index=True, null=True)),
                ('import_date', models.DateTimeField(blank=True, null=True)),
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField()),
                ('url', models.URLField()),
                ('stream', models.CharField(max_length=100, blank=True, null=True)),
                ('chat', models.CharField(max_length=100, blank=True, null=True)),
                ('type', models.CharField(max_length=3, choices=[('POD', 'Podcast'), ('EVT', 'Event'), ('RAD', 'Radio')])),
                ('deleted', models.BooleanField(default=False)),
                ('approved', models.BooleanField(default=False)),
                ('create_date', models.DateTimeField(default=datetime.datetime.now)),
                ('cover', models.ForeignKey(to='snotes20.Cover', blank=True, related_name='podcasts', null=True)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
                ('mums', models.ManyToManyField(to=settings.AUTH_USER_MODEL, related_name='mum_podcasts')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Podcaster',
            fields=[
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('uri', models.URLField(db_index=True, unique=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PodcastSlug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('slug', models.SlugField(unique=True)),
                ('date_added', models.DateTimeField(default=datetime.datetime.now)),
                ('podcast', models.ForeignKey(to='snotes20.Podcast', related_name='slugs')),
            ],
            options={
                'get_latest_by': 'date_added',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('create_date', models.DateTimeField()),
                ('comment', models.CharField(max_length=250, blank=True, null=True)),
                ('preliminary', models.BooleanField(default=False)),
                ('creator', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='created_publications')),
                ('episode', models.ForeignKey(to='snotes20.Episode', related_name='publications')),
                ('podcasters', models.ManyToManyField(to='snotes20.Podcaster', blank=True, related_name='contributed_publications')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PublicationRequest',
            fields=[
                ('id', django_extensions.db.fields.PostgreSQLUUIDField(blank=True, primary_key=True, editable=False, name='id', serialize=False)),
                ('create_date', models.DateTimeField()),
                ('comment', models.CharField(max_length=250, blank=True, null=True)),
                ('episode', models.ForeignKey(to='snotes20.Episode', related_name='publicationrequests')),
                ('requester', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='requested_publicationrequests')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RawPodcaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=150, validators=[django.core.validators.MinLengthValidator(2)])),
                ('meta', models.ForeignKey(to='snotes20.DocumentMeta', related_name='podcasters')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Shownoter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=150, blank=True, null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, blank=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TextDocumentState',
            fields=[
                ('documentstate_ptr', models.OneToOneField(to='snotes20.DocumentState', primary_key=True, auto_created=True, parent_link=True, serialize=False)),
                ('text', models.TextField()),
            ],
            options={
            },
            bases=('snotes20.documentstate',),
        ),
        migrations.AddField(
            model_name='publication',
            name='raw_state',
            field=models.OneToOneField(to='snotes20.TextDocumentState', related_name='publication_raw'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='shownoters',
            field=models.ManyToManyField(to='snotes20.Shownoter', blank=True, related_name='contributed_publications'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='publication',
            name='state',
            field=models.OneToOneField(to='snotes20.DocumentState', related_name='publication'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='osfnote',
            name='tags',
            field=models.ManyToManyField(to='snotes20.OSFTag', related_name='notes'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='osfnote',
            unique_together=set([('order', 'state')]),
        ),
        migrations.AddField(
            model_name='nusersocial',
            name='type',
            field=models.ForeignKey(to='snotes20.NUserSocialType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='nusersocial',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='socials'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='nusersocial',
            unique_together=set([('user', 'type')]),
        ),
        migrations.AddField(
            model_name='importerdatasourcelog',
            name='log',
            field=models.ForeignKey(to='snotes20.ImporterLog', related_name='sources'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='episode',
            name='podcast',
            field=models.ForeignKey(to='snotes20.Podcast', related_name='episodes'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentstateerror',
            name='state',
            field=models.ForeignKey(to='snotes20.DocumentState', related_name='errors'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documentmeta',
            name='shownoters',
            field=models.ManyToManyField(to='snotes20.Shownoter', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='meta',
            field=models.OneToOneField(to='snotes20.DocumentMeta', blank=True, related_name='document', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='raw_state',
            field=models.ForeignKey(to='snotes20.TextDocumentState', blank=True, related_name='rdocument', on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='document',
            name='state',
            field=models.ForeignKey(to='snotes20.DocumentState', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='document',
            field=models.ForeignKey(to='snotes20.Document', related_name='messages'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='issuer',
            field=models.OneToOneField(to='snotes20.ChatMessageIssuer'),
            preserve_default=True,
        ),
    ]
