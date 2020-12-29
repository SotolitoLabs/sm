#!/bin/bash

ACTION=""
DJANGO_CONTAINER=$(podman ps --format '{{.Names}}' --filter "name=django-rest")

if [[ ("${DJANGO_CONTAINER}" == "") && ("${2}" == "") ]]; then
    echo "Django container not running please start the application"
    exit
fi

if [[ "${1}" == "" ]]; then
    echo "Missing action form manage.py aborting..."
    exit
else
    ACTION=$1
fi

if [[ "${2}" != "" ]]; then
    DJANGO_CONTAINER=$2
fi


echo "Executing src/sm/manage.py ${ACTION}"

podman exec -ti ${DJANGO_CONTAINER} /code/sm/manage.py ${ACTION}
