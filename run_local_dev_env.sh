#!/bin/bash

# (c) 2020 SotolitoLabs
# Iván Chavero <ichavero@chavero.com.mx>
# 
# This program runs a podman/kubernetes manifest from a directory
# the it will concatenate the first argument to the MANIFEST_PREFIX
# variable tha will complete the manifest name
# The second argument will set the django superuser password



MANIFEST_PREFIX="django-env"
PODS="infra/pods"
HOST="localhost"
WAIT_TIME=10
SUPERUSER_NAME="sotolito_admin"
SUPERUSER_EMAIL="info@sotolitolabs.com"
SUPERUSER_PW="prueba123"
DEBUG=false
PG_CONTAINER="django-postgres"
DJANGO_CONTAINER="django-rest"
POD_NAME=$MANIFEST_PREFIX

pod=$(podman pod ps --format '{{.Name}}' --filter "name=${POD_NAME}")

if [[ "${1}" == "--help" ]]; then
    echo "Usage: $0 <manifest hostname> <django superuser password>"
    exit
fi


if [[ "${pod}" == "django-env" ]]; then
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
        ready=$(podman exec -ti ${PG_CONTAINER} /usr/bin/pg_isready 2>&1)
        if [[ ${DEBUG} == true ]]; then
            echo "READY: ${ready}"
        fi
      echo -n "."
    done
    echo
    echo "PostgreSQL database ready"
}


function run_pod {
  echo "Creating pod ${POD_NAME} manually"
  podman pod create -n ${POD_NAME} -p 8081:80

  echo "Starting postgres" 
  podman run -d --name=django-postgres --rm --pod ${POD_NAME} \
    -e DJANGO_DB=test_db --pod ${POD_NAME} \
    -e DJANGO_DB_USER=test_user \
    -e DJANGO_PASSWORD=prueba123 \
    -e POSTGRES_PASSWORD=prueba123  \
    -v /home/ichavero/tmp/salud_mental/django-postgres:/var/lib/postgresql/data \
    quay.io/sotolitolabs/django-postgresql:latest

  echo "Starting django app"
  podman run -d --name=django-rest --rm --pod ${POD_NAME} \
    -v /home/ichavero/sotolitoLabs/sm/src:/code \
    quay.io/sotolitolabs/django-rest:latest \
    /code/run_uwsgi.sh

  echo "Starting starting nginx"
  podman run -d --name=django-nginx --rm --pod ${POD_NAME} \
    -v /home/ichavero/sotolitoLabs/sm/src/sm/static:/usr/share/nginx/html \
    quay.io/sotolitolabs/django-rest-nginx:latest


  #DISABLED FOR NOWpodman play kube ${PODS}/${MANIFEST_PREFIX}-${HOST}.yaml
}

echo "Starting development environment for ${HOST}"
run_pod

PG_CONTAINER=$(podman ps --format '{{.Names}}' --filter "name=postgres")
DJANGO_CONTAINER=$(podman ps --format '{{.Names}}' --filter "name=django-rest")

if [[ $? != 0 ]]; then
    echo "Error creating pod $!"
    exit
fi

echo "Checking pods:"
podman pod ps

echo "Checking containers"
podman ps -a --format '{{ .ID }} {{ .Names }}  {{ .Ports }} {{ .Pod }}'

echo "Waiting for the database to come up"

# Get the container name because in some systems the pod name gets concatenated
# to the container name
PG_CONTAINER=$(podman ps --filter 'name=postgres' --format '{{.Names}}')
wait_for_postgres



echo "DJANGO: $DJANGO_CONTAINER"
echo "Running migrations in ${DJANGO_CONTAINER}"
podman exec -ti ${DJANGO_CONTAINER} /code/sm/manage.py migrate

echo "Creating superuser"
res=$(podman exec -e "DJANGO_SUPERUSER_PASSWORD=${SUPERUSER_PW}" -ti ${DJANGO_CONTAINER} /code/sm/manage.py createsuperuser  --no-input --username=${SUPERUSER_NAME} --email=${SUPERUSER_EMAIL} 2>&1)

if [[ ${res} == *"successfully"* ]]; then
  echo $res
else
  echo "Superuser ${SUPERUSER_NAME} already created"
fi

