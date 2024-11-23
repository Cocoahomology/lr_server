#!/bin/sh

# Exit immediately if a command exits with a non-zero status.
set -e

# Run database migrations
python manage.py makemigrations
python manage.py migrate

# Create a superuser with username and password 'admin' if it doesn't exist
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ]; then
    python manage.py shell -c "from django.contrib.auth.models import User; User.objects.filter(username=\"$DJANGO_SUPERUSER_USERNAME\").exists() or User.objects.create_superuser(\"$DJANGO_SUPERUSER_USERNAME\", \"$DJANGO_SUPERUSER_EMAIL\", \"$DJANGO_SUPERUSER_PASSWORD\")"
fi

# Start the Django development server with SSL
python manage.py runserver_plus --cert-file /app/certs/server.crt --key-file /app/certs/server.key 0.0.0.0:8000

# Execute the command passed to the script
exec "$@"