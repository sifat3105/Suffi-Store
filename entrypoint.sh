#!/bin/sh

echo "🚀 Starting Django entrypoint..."

# Apply database migrations
echo "📌 Applying migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📌 Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn server
echo "📌 Starting Gunicorn..."
gunicorn project.wsgi:application --bind 0.0.0.0:8000 --workers 4
