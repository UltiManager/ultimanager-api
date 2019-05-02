#!/bin/sh

set -euf

MANAGE_PATH=/opt/ultimanager-web/ultimanager/manage.py
MANAGE_CMD="python $MANAGE_PATH"

# Get sentry to generate a release version based on the current commit
# hash.
VERSION="ultimanager-web@$(cat /opt/ultimanager-web/VERSION)"
echo "Running ${VERSION}"

export SENTRY_RELEASE=${VERSION}

create_db_user() {
    # Note that the tabs in the following statement are used to preserve
    # indentation in the SQL statements.
    CREATE_ROLE=$(cat <<-EOF
		DO \$\$
		BEGIN
		    CREATE ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}';
		    EXCEPTION WHEN OTHERS THEN
			    RAISE NOTICE 'not creating role ${DB_USER} -- it already exists';
			    ALTER ROLE ${DB_USER} WITH LOGIN PASSWORD '${DB_PASSWORD}';
			    RAISE NOTICE 'Set password for role ${DB_USER}';
		END
		\$\$;
	EOF
	)

    export PGPASSWORD=${DATABASE_ADMIN_PASSWORD}
	echo ${CREATE_ROLE} | psql --host ${DB_HOST} --port ${DB_PORT} --user ${DATABASE_ADMIN_USER} --dbname ${DB_NAME}
}

if [[ "$1" = 'background-jobs' ]]; then
    echo "No background jobs to run."
    exit 0
fi

if [[ "$1" = 'migrate' ]]; then
    create_db_user
    ${MANAGE_CMD} migrate
    ${MANAGE_CMD} collectstatic --no-input
    exit 0
fi

if [[ "$1" = 'server' ]]; then
    # First shift to pop 'server' off the arg list. The rest of the arguments
    # are passed as-is to Gunicorn.
    shift
    cd /opt/ultimanager-web/ultimanager
    exec gunicorn ultimanager.wsgi:application $@
fi

if [[ "$1" = '' ]]; then
    echo "No command provided."
    exit 1
fi

echo "Unrecognized command: $1"
exit 1
