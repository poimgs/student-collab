#!/bin/sh

echo "Running migrations"
python manage.py migrate --no-input

echo "Creating superuser"
python manage.py createsuperuser --noinput

echo "Collecting static files"
python manage.py collectstatic --no-input

echo "Running Django server"
python manage.py runserver 0.0.0.0:8000

