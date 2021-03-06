#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "rolca.settings_rolcabox")

    if len(sys.argv) == 2 and sys.argv[1] == 'runserver':
        sys.argv.append('0.0.0.0:8000')

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
