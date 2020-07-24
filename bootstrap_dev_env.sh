#!/bin/bash

CONTAINER="django-env-django-rest"

if [[ "${1}" != "" ]]; then
    CONTAINER=$1
fi

podman exec -ti ${CONTAINER} /code/prepare_dev_env.sh
