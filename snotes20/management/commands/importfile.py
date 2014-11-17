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


"""
config file:

{
    "csv_file": "path to csv file",
    "data_dir": "path to txt file directory",
    "exluded_podcasts": [
        "podcast slug to ignore",
    ],
    "exclude": {
        "deleted": true,
        "nopodcast": true,
        "private": true
    },
     "add_slugs": [
        {
            "existing": "slug to search",
            "added": "slug to add to found podcast"
        }
    ],
    "add_podcasts": [
        {
            "slug": "",
            "title": "",
            "description": "",
            "url": "",
            "type": "POD"
        }
    ]
}

csv file:
filename,,podcast-slug,number,delete,no-podcast,private,hoerid
"""




class Command(BaseCommand):
    args = ''
    help = ''

    @transaction.atomic
    def handle(self, *args, **options):
        if len(args) != 1:
            print("supply config file")
            return

        config = json.load(open(args[0], 'r'))

        existingmode = config['options']['existingmode']
        nameprefix = config['options']['nameprefix']

        print("Add podcasts")
        for pod in config['add_podcasts']:
            if  models.PodcastSlug.objects.all().filter(slug=pod['slug']).exists():
                print('skip already present: ' + pod['slug'])
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

            print('[+] added: ' + pod['slug'])

        print("[ ] Add slugs")
        for slug in config['add_slugs']:
            if  models.PodcastSlug.objects.all().filter(slug=slug['added']).exists():
                print('[?] skip already present: ' + slug['added'])
                continue

            try:
                db_pod = models.Podcast.objects.get(slugs__slug=slug['existing'])
            except models.Podcast.DoesNotExist:
                print('[?] cannot add : ' + slug['added'] + ', existing slug not found')
                continue

            db_slug = models.PodcastSlug(slug=slug['added'], podcast=db_pod)
            db_slug.save()

            db_pod.slugs.add(db_slug)
            db_pod.save()

            print('[+] added: ' + slug['added'])


        print("[ ] Add episodes")
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

                print('[ ] Importing: ' + pad_name)

                try:
                    with open(full_file, 'r') as ff:
                        file_content = ff.read()
                except:
                    print("[!] cannot load file")
                    continue

                file_lines = [line.rstrip('\r') for line in file_content.split('\n')]

                print("[+] file loaded got " + str(len(file_lines)) + " lines")

                if config['exclude']['deleted'] and is_deleted:
                    print('[?] skip (deleted)')
                    continue
                if config['exclude']['private'] and is_private:
                    print('[?] skip (private)')
                    continue
                if config['exclude']['nopodcast'] and not is_podcast:
                    print('[?] skip (no podcast)')
                    continue
                if pod in config['exluded_podcasts']:
                    print('[?] skip (excluded podcast)')
                    continue

                header, parse_lines = osf.parse_lines(file_lines)
                osf_lines = osf.objectify_lines(parse_lines)

                status = 'broken' if any(isinstance(line, modgrammar.ParseError) for line in osf_lines) else 'ok'

                print(status)


                try:
                    db_pod = models.Podcast.objects.get(slugs__slug=pod)
                except models.Podcast.DoesNotExist:
                    print('[!] cannot find podcast: ' + pod)
                    return

                with transaction.atomic():
                    meta = models.DocumentMeta()
                    meta.save()

                    doc_name = "pp_" + pad_name

                    try:
                        db_doc = models.Document.objects.get(name=doc_name)

                        if existingmode == 'skip':
                            print('[?] skip (existing)')
                            continue
                        elif existingmode == 'delete':
                            db_doc.remove()
                            raise models.Document.DoesNotExist()
                        elif existingmode == 'update':
                            pass
                        else:
                            print('[!] unknown existingmode, aborting import')
                            return
                    except models.Document.DoesNotExist:
                        db_doc = models.Document()

                    db_doc.name = nameprefix + pad_name
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

                print('[+] imported')
