#!/bin/bash

echo "Stopping development envirnment"
podman pod stop django-env
podman pod rm django-env
