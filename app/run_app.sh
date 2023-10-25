#!/bin/sh

python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput  # need to gunicorn download static
gunicorn --access-logfile - --workers 1 --timeout 20 --reload \
  --bind app:8000 core.wsgi:application
