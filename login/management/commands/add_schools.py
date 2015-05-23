"""
====================
Command: add_schools
====================

"""
import os

from django.core.management.base import BaseCommand, CommandError

from login.models import Institution


class Command(BaseCommand):

    help = 'Add list of institutions to database.'

    def add_arguments(self, parser):
        parser.add_argument(
            'file_names',
            nargs='+',
            default=False,
            help='List of files to import.'),
        parser.add_argument(
            '-r', '--replace',
            action='store_true',
            help='Deactivate not listed entries.'),

    def handle(self, *args, **options):
        if options['replace']:
            # TODO: implement
            raise CommandError('Option is not implemented yet.')

        for file_name in options['file_names']:
            if not os.path.isfile(file_name):
                raise CommandError('{} does not exists.'.format(file_name))

        for file_name in options['file_names']:
            with open(file_name) as in_file:
                for line in in_file.readlines():
                    line = line.rstrip()

                    if line is "" or len(Institution.objects.filter(name=line)) > 0:
                        continue

                    Institution.objects.create(name=line)
                    if options['verbosity'] > 1:
                        self.stdout.write("Added {} to database.".format(line))
