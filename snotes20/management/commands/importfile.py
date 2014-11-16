import logging
import json
import csv
import sys
import os
import osf
import modgrammar

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import snotes20.models as models
import snotes20.editors as editors
import snotes20.contenttypes as contenttypes

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = ''

    @transaction.atomic
    def handle(self, *args, **options):
        if len(args) != 1:
            print("supply config file")
            return

        config = json.load(open(args[0], 'r'))

        for pod in config['add_podcasts']:
            if  models.PodcastSlug.objects.all().filter(slug=pod['slug']).exists():
                print('skipping podcast: ' + pod['slug'])
                continue

            db_pod = models.Podcast()
            db_pod.title = pod['title']
            db_pod.description = pod['description']
            db_pod.url = pod['url']
            db_pod.type = pod['type']
            db_pod.save()

            db_slug = models.PodcastSlug(slug=pod['slug'], podcast=db_pod)
            db_slug.save()

            db_pod.slugs.add(db_slug)
            db_pod.save()

        with open(config['csv_file']) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader, None)

            for row in reader:
                file = row[0]
                pad_name = file.split('.')[0]
                full_file = config['data_dir'] + "/" + file

                pod = row[2]
                number = row[3]

                is_deleted = (row[4] == 'x')
                is_podcast = not (row[5] == 'x')
                is_private = (row[6] == 'x')

                hoerid = row[7]

                with open(full_file, 'r') as ff:
                    file_content = ff.read()

                file_lines = [line.rstrip('\r') for line in file_content.split('\n')]

                print('[ ] File: ' + file + ' ')


                print('  - loading: ', end='')

                if config['exclude']['deleted'] and is_deleted:
                    print('skip (deleted)')
                    continue
                if config['exclude']['private'] and is_private:
                    print('skip (private)')
                    continue
                if config['exclude']['nopodcast'] and not is_podcast:
                    print('skip (no podcast)')
                    continue
                if pod in config['exluded_podcasts']:
                    print('skip (excluded podcast)')
                    continue

                print('ok')


                print('  - loading: ', end='')

                header, parse_lines = osf.parse_lines(file_lines)
                osf_lines = osf.objectify_lines(parse_lines)

                status = 'broken' if any(isinstance(line, modgrammar.ParseError) for line in osf_lines) else 'ok'

                print(status)


                print('  - importing: ', end='')

                try:
                    db_pod = models.Podcast.objects.get(slugs__slug=pod)
                except models.Podcast.DoesNotExist:
                    print('[!] couldn\'t find podcast: ' + pod)
                    return

                with transaction.atomic():
                    meta = models.DocumentMeta()
                    meta.save()

                    doc_name = "pp_" + pad_name

                    try:
                        db_doc = models.Document.objects.get(name=doc_name)
                    except models.Document.DoesNotExist:
                        db_doc = models.Document()

                    db_doc.name = "pp_" + pad_name
                    db_doc.editor = models.EDITOR_ETHERPAD
                    db_doc.meta = meta
                    db_doc.save()

                    editor = editors.EditorFactory.get_editor(db_doc.editor)
                    editor.set_document_text(db_doc, file_content)

                    try:
                        db_ep = models.Episode.objects.get(document=db_doc)
                    except models.Episode.DoesNotExist:
                        db_ep = models.Episode()

                    db_ep.podcast = db_pod
                    db_ep.document = db_doc
                    db_ep.number = number

                    if len(hoerid) > 0:
                        db_ep.source = models.SOURCE_HOERSUPPE
                        db_ep.source_id = hoerid

                    db_ep.save()

                print('ok')
