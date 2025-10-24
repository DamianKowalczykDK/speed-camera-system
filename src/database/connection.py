from mysql.connector import pooling, MySQLConnection
from typing import Callable, Any, cast
from dotenv import load_dotenv
import os

load_dotenv()

class MySQLConnectionManager:
    def __init__(self):
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
        return self._pool.get_connection()

def with_db_connection(func: Callable) -> Callable:
    def wrapper(self, *args: Any, conn: MySQLConnection | None = None, **kwargs: Any) -> Any:

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