#!/bin/sh
# Wait for DB if needed
echo "Waiting for DB at $DB_HOST:$DB_PORT..."
sleep 10  # or use wait-for-it.sh for smarter wait

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Start the server (adjust for production)
gunicorn RRMSAPI.wsgi:application --bind 0.0.0.0:8001
