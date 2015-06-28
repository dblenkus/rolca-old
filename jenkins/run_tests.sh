#!/bin/bash

echo "Prepairing virtualenv..."
export DJANGO_SETTINGS_MODULE=rolca.settings_rolcatest
VENV_HOME=$WORKSPACE/.venv/
rm -rf $VENV_HOME
virtualenv $VENV_HOME
. $VENV_HOME/bin/activate
pip install -r requirements.txt >/dev/null

./manage.py makemigrations
./manage.py migrate  --noinput
./manage.py collectstatic --noinput >/dev/null
./manage.py jenkins --enable-coverage --noinput

cloc --exclude-dir=bower_components,.venv,media,static,reports,docs --by-file --xml --out=reports/cloc.xml .
