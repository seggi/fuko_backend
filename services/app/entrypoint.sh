#!/bin/sh

if [ "$DATABASE" = "postgres" ]

then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done
    echo "PostgreSQL started"
fi

if [ "$FLASK_CONFIG" = "production" ]
echo "You are in production mode"
export FLASK_APP="/home/app/manage.py"
then
    echo "Tables created"
fi

exec "$@"
