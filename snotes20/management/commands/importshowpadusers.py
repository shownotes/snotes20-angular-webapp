import logging
import datetime
import json

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

import snotes20.models as models

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    args = ''
    help = ''

    @transaction.atomic
    def handle(self, *args, **options):
        if len(args) != 1:
            print("supply config file")
            return

        users = json.load(open(args[0], 'r'))

        for user in users:
            username = str(user['username'])

            if user['status'] != 'normal':
                print('skipped abnormal user {} ({})'.format(username, user['status']))
                continue
            if models.NUser.objects.filter(username=username).exists():
                print('skipped existing ' + username)
                continue

            emailTokens = user['activateEmailTokens']

            # fix manually activated users
            if user['email'] is None and len(emailTokens.keys()) == 1:
                user['email'] = emailTokens[list(emailTokens.keys())[0]]['email']

            nuser = models.NUser()
            nuser.username = username
            nuser.old_password = user['salt'] + '$' + str(user['iterations']) + '$' + user['password']
            nuser.date_joined = datetime.date.fromtimestamp(int(user['createTime']/1000))
            nuser.migrated = False
            nuser.is_active = True
            nuser.email = user['email']
            nuser.save()

            print('imported ' + username)
