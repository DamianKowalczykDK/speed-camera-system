from src.database.connection import MySQLConnectionManager, with_db_connection
from mysql.connector.connection import MySQLCursor, MySQLConnection
from mysql.connector import Error
from src.config import logger


class SqlFileExecutor:
    """Executes SQL commands from a .sql file using a managed MySQL connection.

    This class provides functionality for reading SQL scripts from files and
    executing them sequentially within a managed database connection.
    It uses the `with_db_connection` decorator to ensure safe transaction handling.
    """

    def __init__(self, connection_manager: MySQLConnectionManager):
        """Initializes the SQL file executor with a connection manager.

        Args:
            connection_manager (MySQLConnectionManager): The manager responsible
                for providing MySQL connections from a connection pool.
        """
        self._connection_manager = connection_manager
        self._conn: MySQLConnection
        self._cursor: MySQLCursor

    @with_db_connection
    def execute_sql_file(self, file_path: str) -> None:
        """Executes all SQL commands found in a given .sql file.

        The method reads the contents of a .sql file, splits it by semicolons,
        and executes each command sequentially. Transactions and error handling
        are managed by the `with_db_connection` decorator.

        Args:
            file_path (str): The path to the .sql file containing SQL commands.

        Raises:
            mysql.connector.Error: If any SQL command fails to execute.
        """
        with open(file_path, 'r') as sql_file:
            sql_commands = sql_file.read()

        try:
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:
                    logger.info(f'Executing command: {command}')
                    self._cursor.execute(command)
        except Error as e:
            logger.error(f'Error while executing sql file: {e}')
            raise e