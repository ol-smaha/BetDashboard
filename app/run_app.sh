#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic   # need to gunicorn download static
gunicorn --access-logfile - --workers 4 --timeout 300 --reload \
  --bind app:8000 core.wsgi:application
