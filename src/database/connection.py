from mysql.connector import pooling, MySQLConnection
from typing import Callable, Any, cast
from dotenv import load_dotenv
import os

load_dotenv()

class MySQLConnectionManager:
    """Manages a pool of MySQL connections using mysql.connector.pooling.

    This class initializes a connection pool based on environment variables
    and provides pooled connections to the database when requested.
    """

    def __init__(self):
        """Initializes the MySQL connection pool using environment variables.

        Environment variables:
            DB_POOL_SIZE: Number of connections in the pool (default: 5).
            DB_HOST: Database host.
            DB_NAME: Database name.
            DB_USER: Database username.
            DB_PASSWORD: Database password.
            DB_PORT: Database port (default: 3307).
        """
        self._pool = pooling.MySQLConnectionPool(
            pool_name='localhost',
            pool_size=int(os.getenv('DB_POOL_SIZE', 5)),
            host=os.getenv('DB_HOST'),
            database=os.getenv('DB_NAME'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            port=int(os.getenv('DB_PORT', 3307)),
        )

    def get_connection(self) -> MySQLConnection:
        """Retrieves a new database connection from the connection pool.

        Returns:
            MySQLConnection: A MySQL database connection object.
        """
        return self._pool.get_connection()


def with_db_connection(func: Callable) -> Callable:
    """Decorator for managing MySQL connections and transactions.

    This decorator ensures that a database connection and cursor are available
    for the wrapped function. It supports both internal (managed) and external
    connections, handling commits, rollbacks, and proper cleanup.

    Args:
        func (Callable): The function to wrap, which expects `self` and optional
            database-related arguments.

    Returns:
        Callable: The wrapped function with automatic connection and transaction handling.
    """
    def wrapper(self, *args: Any, conn: MySQLConnection | None = None, **kwargs: Any) -> Any:
        """Wrapper providing automatic connection handling for the decorated method."""
        external_conn = conn is not None
        if not external_conn:
            conn = self._connection_manager.get_connection()

        conn = cast(MySQLConnection, conn)

        with conn.cursor() as cursor:
            try:
                self._conn = conn
                self._cursor = cursor
                result = func(self, *args, **kwargs)

                if not external_conn:
                    self._conn.commit()

                return result
            except Exception as e:
                if not external_conn and self._conn:
                    self._conn.rollback()
                raise e
            finally:
                if not external_conn and conn:
                    conn.close()

    return wrapper