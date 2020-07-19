#!/bin/bash

CONTAINER="django-rest"

if [[ "${1}" != "" ]]; then
    CONTAINER=$1
fi


echo "Starting shell in ${CONTAINER} container"

podman exec -ti ${CONTAINER} /bin/sh
