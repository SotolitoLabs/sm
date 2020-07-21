#!/bin/sh

# FIXME Add later --env DJANGO_SETTINGS_MODULE=sm.settings \

echo "Collect static files"
/code/sm/manage.py collectstatic

echo "Running production sm application"
uwsgi --chdir=/code/sm \
    --module=sm.wsgi:application \
    --master --pidfile=/tmp/sm-master.pid \
    --socket=127.0.0.1:8000 \
    --processes=2 \
    --uid=1000 --gid=2000 \
    --harakiri=20 \
    --max-requests=5000 \
    --touch-reload=/code/reload.me \
    --vacuum
