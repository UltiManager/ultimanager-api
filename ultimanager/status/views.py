from django.db import DEFAULT_DB_ALIAS, connections
from django.db.migrations.executor import MigrationExecutor
from django.http import HttpResponse


def health_check(_):
    """
    Check the status of the application. A 200 response will be returned
    if the application is healthy.
    """
    # The following code is taken from:
    # https://engineering.instawork.com/elegant-database-migrations-on-ecs-74f3487da99f
    executor = MigrationExecutor(connections[DEFAULT_DB_ALIAS])
    plan = executor.migration_plan(executor.loader.graph.leaf_nodes())
    status = 503 if plan else 200

    return HttpResponse(status=status)
