#!/bin/sh
set -e

echo "🟡 Waiting for Postgres Database Startup ($POSTGRES_HOST $POSTGRES_PORT)..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 2
done

echo "✅ Postgres Database Started Successfully ($POSTGRES_HOST:$POSTGRES_PORT)"

python manage.py collectstatic --noinput

python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
