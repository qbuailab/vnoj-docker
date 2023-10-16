# Copy to dmoj/repo/judge/management/commands/cus_batchadduser.py

import csv
import secrets
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from judge.models import Language, Profile, Organization


def add_user(username, fullname, password, about, organization):
    usr = User.objects.update_or_create(username=username, defaults={
                                   'first_name': fullname,
                                   'is_active': True
                               })[0]
    usr.set_password(password)
    usr.save()

    profile = Profile.objects.update_or_create(user=usr, defaults={
        "about": about
        })[0]
    profile.language = Language.objects.get(key=settings.DEFAULT_USER_LANGUAGE)
    profile.organizations.set(organization)
    profile.save()


class Command(BaseCommand):
    help = 'batch create users with about and organization'

    def add_arguments(self, parser):
        parser.add_argument('input', help='csv file containing username, fullname, and about information')
        parser.add_argument('orgid', help='id of organization.')
        parser.add_argument('output', help='where to store output csv file')

    def handle(self, *args, **options):
        fin = open(options['input'], 'r')
        fout = open(options['output'], 'w', newline='')
        organization = Organization.objects.get(pk=int(options['orgid']))
        reader = csv.DictReader(fin)
        writer = csv.DictWriter(fout, fieldnames=['username', 'fullname', 'about', 'password'])
        writer.writeheader()

        for row in reader:
            username = row['username']
            fullname = row['fullname']
            about = row['about']
            password = "QbuOJ@1234"

            add_user(username, fullname, password, about, [organization])

            writer.writerow({
                'username': username,
                'fullname': fullname,
                'about': about,
                'password': password,
            })

        fin.close()
        fout.close()
