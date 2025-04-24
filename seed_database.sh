#!/bin/bash

rm db.sqlite3
rm -rf ./GearSpotapi/migrations
python3 manage.py migrate
python3 manage.py makemigrations GearSpotapi
python3 manage.py migrate GearSpotapi
python manage.py loaddata users.json
python manage.py loaddata profiles.json
python manage.py loaddata posts.json
python manage.py loaddata comments.json
python manage.py loaddata tags.json
python manage.py loaddata posttags.json
python manage.py loaddata likes.json
python manage.py loaddata tokens.json

