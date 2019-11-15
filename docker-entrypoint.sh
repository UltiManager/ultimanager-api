#!/bin/sh

set -euf

MANAGE_PATH=/opt/ultimanager-api/ultimanager/manage.py
MANAGE_CMD="python $MANAGE_PATH"

create_db() {
    CREATE_DB="SELECT 'CREATE DATABASE ${DB_NAME}' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '${DB_NAME}')\gexec"

    export PGPASSWORD=${DB_PASSWORD}
    echo ${CREATE_DB} | psql --host ${DB_HOST} --port ${DB_PORT} --user ${DB_USER} --dbname postgres
}

if [[ "$1" = 'background-jobs' ]]; then
    echo "No background jobs to run."
    exit 0
fi

if [[ "$1" = 'migrate' ]]; then
    create_db
    ${MANAGE_CMD} migrate
    ${MANAGE_CMD} collectstatic --no-input
    exit 0
fi

if [[ "$1" = 'server' ]]; then
    # First shift to pop 'server' off the arg list. The rest of the arguments
    # are passed as-is to Gunicorn.
    shift
    cd /opt/ultimanager-api/ultimanager
    exec gunicorn ultimanager.wsgi:application $@
fi

if [[ "$1" = '' ]]; then
    echo "No command provided."
    exit 1
fi

echo "Unrecognized command: $1"
exit 1
