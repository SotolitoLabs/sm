#!/bin/bash

PODS="infra/pods"
HOST="local"
CONTAINER="django-rest"
WAIT_TIME=10
SUPERUSER_NAME="sotolito_admin"
SUPERUSER_EMAIL="info@sotolitolabs.com"
SUPERUSER_PW="prueba123"


pod=$(podman pod ps --format '{{.Name}}' --filter "name=django-env")

if [[ ${pod} == "django-env" ]]; then
  echo "Development environment already running, use ./stop_dev_env.sh to stop it or cleanup"
  exit
fi

if [[ "${1}" != "" ]]; then
    HOST=$1
fi

if [[ "${2}" != "" ]]; then
    SUPERUSER_PW=$2
fi

function wait_for_postgres {
    ready=""
    while [[ ${ready} != *"accepting connections"* ]]; do
      ready=$(podman exec -ti django-postgres /usr/bin/pg_isready 2>&1)
      echo -n "."
    done
    echo
    echo "PostgreSQL database ready"
}

echo "Starting development environment for $1"
podman play kube ${PODS}/django-env-${HOST}.yaml

echo "Checking pods:"
podman pod ps

echo "Checking containers"
podman ps -a --format '{{ .ID }} {{ .Names }}  {{ .Ports }} {{ .Pod }}'

echo "Waiting for the database to come up"
wait_for_postgres

echo "Running migrations"
podman exec -ti ${CONTAINER} /code/sm/manage.py migrate

echo "Creating superuser"
res=$(podman exec -e "DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PW}" -ti ${CONTAINER} /code/sm/manage.py createsuperuser  --no-input --username=${SUPERUSER_NAME} --email=${SUPERUSER_EMAIL} 2>&1)

if [[ ${res} == *"successfully"* ]]; then
  echo $res
else
  echo "Superuser ${SUPERUSER_NAME} already created"
fi

