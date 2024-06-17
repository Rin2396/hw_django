"""Runner for tests."""
from types import MethodType
from typing import Any

from django.db import connections
from django.db.backends.base.base import BaseDatabaseWrapper
from django.test.runner import DiscoverRunner


def prepare_db(self):
    """Ensure the 'game_site' schema exists in the database.

    Args:
        self (class): class
    """
    self.connect()
    self.connection.cursor().execute('CREATE SCHEMA IF NOT EXISTS game_site;')


class PostgresSchemaRunner(DiscoverRunner):
    """Custom Django test runner for PostgreSQL with schema preparation."""

    def setup_databases(self, **kwargs: Any) -> list[tuple[BaseDatabaseWrapper, str, bool]]:
        """Override to prepare database schemas before setting up databases.

        Args:
            kwargs: Additional keyword arguments.

        Returns:
            list: List of database configurations.
        """
        for conn_name in connections:
            connection = connections[conn_name]
            connection.prepare_database = MethodType(prepare_db, connection)
        return super().setup_databases(**kwargs)
