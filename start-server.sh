#!/bin/bash
# start-server.sh
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --no-input

if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (python manage.py createsuperuser --no-input)
fi
(gunicorn easyline.wsgi:application --bind 0.0.0.0:8001 --workers 3) & (python server_websocket.py) & 
nginx -g "daemon off;"