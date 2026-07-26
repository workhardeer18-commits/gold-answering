#!/bin/sh

set -e
cd gold
echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

case "$1" in

  web)
    echo "Starting Gunicorn..."
    gunicorn gold.wsgi:application --bind 0.0.0.0:8000 --workers 3 --timeout 120
    ;;

#  worker)
#    echo "Starting Celery Worker..."
#    celery -A gold worker \
#        --loglevel=info
#    ;;
#
#  beat)
#    echo "Starting Celery Beat..."
#    celery -A gold beat --loglevel=info
#    ;;

esac

