"""Wrapper over the psycopg2 module.
"""

import logging
import psycopg2
import psycopg2.extras


psycopg2.extras.register_uuid()

LOG = logging.getLogger('postgres')


class Connection:

    def __init__(self, user, database):
        self.connection = psycopg2.connect(
            user=user,
            database=database,
            cursor_factory=psycopg2.extras.RealDictCursor,
        )

    def query(self, *execute_args):
        """Makes a request for data.
        """

        return self._execute(True, *execute_args)

    def non_query(self, *execute_args):
        """Updates the database.
        """

        return self._execute(False, *execute_args)

    def _execute(self, is_query, *execute_args):
        """Executes the given commands.
        """

        with self.connection.cursor() as cursor:
            try:
                cursor.execute(*execute_args)
                if is_query:
                    result = cursor.fetchall()
                else:
                    result = True
                self.connection.commit()
                return result
            except Exception as exc:
                self.connection.rollback()
                LOG.error('Error executing query\n{}\nException:\n{}'.format(
                    cursor.mogrify(*execute_args), exc))
                return None if is_query else False
