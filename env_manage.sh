#!/bin/bash

ACTION=""
CONTAINER="django-rest"

if [[ "${1}" == "" ]]; then
    echo "Missing action form manage.py aborting..."
    exit
else
    ACTION=$1
fi

if [[ "${2}" != "" ]]; then
    CONTAINER=$2
fi


echo "Executing src/sm/manage.py ${ACTION}"

podman exec -ti ${CONTAINER} /code/sm/manage.py ${ACTION}
