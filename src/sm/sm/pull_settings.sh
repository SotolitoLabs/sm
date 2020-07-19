#!/bin/bash

echo "Pulling changes that include settings.py modifications"

cp settings.py settings.py.dev 
cp settings.py.orig settings.py
git pull
cp settings.py.dev settings.py

echo "Don't forget to add your new upstream setting.py changes to your development settings.py"
