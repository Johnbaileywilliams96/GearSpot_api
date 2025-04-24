#!/bin/bash

rm db.sqlite3
rm -rf ./GearSpotapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations GearSpotapi
python3 manage.py migrate GearSpotapi
python3 manage.py loaddata users
python3 manage.py loaddata tokens

