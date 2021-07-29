#!/usr/bin/env bash
# start-server.sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
(gunicorn easyline.wsgi:application --user www-data --bind 0.0.0.0:8001 --workers 3) &
(gunicorn myproject.asgi:application)
nginx -g "daemon off;"