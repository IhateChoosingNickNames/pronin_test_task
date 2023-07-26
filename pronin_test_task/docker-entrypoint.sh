#!/bin/bash

echo "Apply database migrations"
python manage.py migrate

echo "Starting Gunicorn."
exec gunicorn root.wsgi:application --bind 0.0.0.0:8000 --workers 3
