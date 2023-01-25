#!/bin/sh
set -e
echo "Entrypoint..."
python manage.py wait_for_db
python manage.py collectstatic --no-input
python manage.py migrate
exec "$@"