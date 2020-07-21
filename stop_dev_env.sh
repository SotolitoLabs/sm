#!/bin/bash

echo "Stopping development environment"
podman pod stop django-env
podman pod rm django-env
