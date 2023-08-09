#!/bin/bash

echo "Enabling UnsafeLegacyRenegotiation for pochta.ru"
echo '[openssl_init]
ssl_conf = ssl_sect

[ssl_sect]
system_default = system_default_sect

[system_default_sect]
Options = UnsafeLegacyRenegotiation' >> ~/../usr/lib/ssl/openssl.cnf

echo "Apply database migrations"
python manage.py migrate

echo "Starting Gunicorn."
exec gunicorn root.wsgi:application --bind 0.0.0.0:8000 --workers 3
