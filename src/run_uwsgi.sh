#!/bin/sh

# FIXME Add later --env DJANGO_SETTINGS_MODULE=sm.settings \

echo "Collect static files"
/code/sm/manage.py collectstatic

echo "Ensure the development sqllite database is writable"
chown 1000:2000 /code/sm/db.sqlite3
chgrp 2000 /code/sm
chmod g+rw /code/sm

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
