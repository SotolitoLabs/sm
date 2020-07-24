#!/bin/bash

echo "Setup database"
/code/sm/manage.py makemigrations
/code/sm/manage.py migrate
echo "Create superuser"
/code/sm/manage.py createsuperuser --email admin@sotolitolabs.com --username admin

echo "Ensure the development sqllite database is writable"
chown 1000:2000 /code/sm/db.sqlite3
chgrp 2000 /code/sm
chmod g+rw /code/sm

echo "Reloading changes"
touch /code/reload.me
