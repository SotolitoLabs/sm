#!/bin/bash

PODS="infra/pods"
HOST="local"

if [[ "${1}" != "" ]]; then
    HOST=$1
fi

echo "Starting development environment for $1"
podman play kube ${PODS}/django-env-${HOST}.yaml

echo "Checking pods:"
podman pod ps


echo "Checking containers"
podman ps -a --format '{{ .ID }} {{ .Names }}  {{ .Ports }} {{ .Pod }}'
