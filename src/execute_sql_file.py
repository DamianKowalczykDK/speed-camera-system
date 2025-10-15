from src.database import MySQLConnectionManager, with_db_connection
from mysql.connector.connection import MySQLCursor, MySQLConnection
from mysql.connector import Error


class SqlFileExecutor:
    def __init__(self, connection_manager: MySQLConnectionManager):
        self._connection_manager = connection_manager
        self._conn: MySQLConnection
        self._cursor: MySQLCursor

    @with_db_connection
    def execute_sql_file(self, file_path: str) -> None:
        with open(file_path, 'r') as sql_file:
            sql_commands = sql_file.read()

        try:
            for command in sql_commands.split(';'):
                command = command.strip()
                if command:
                    print(f'Executing command: {command}')
                    self._cursor.execute(command)
        except Error as e:
            print(f'Error while executing sql file: {e}')
            raise e