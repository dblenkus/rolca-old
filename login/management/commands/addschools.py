import os

from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

from ...models import Institution


class Command(BaseCommand):
    args = '<file_path>'
    help = 'Add list of institutions to database.'

    option_list = BaseCommand.option_list + (
        make_option(
            '-r', '--replace',
            action='store_true',
            dest='replace',
            default=False,
            help='Deactivate not listed entries.'),
    )

    def handle(self, *args, **options):
        if len(args) == 0:
            raise CommandError('You have to specify at least one file name.')

        if options['replace']:
            raise CommandError('Option is not implemented yet.')  # TODO: implement

        for fn in args:
            if not os.path.isfile(fn):
                raise CommandError('{} does not exists.'.format(fn))

            with open(fn) as f:  # pylint: disable=invalid-name
                for line in f.readlines():
                    line = line.rstrip('\n')
                    line = line.rstrip('\r')

                    if line is "" or len(Institution.objects.filter(name=line)) > 0:
                        continue

                    Institution.objects.create(name=line)
                    # print u'Added {} to database.'.format(line)
