from src.domain.typed_dict import DriverOffensesDict, TopDriverDict, PopularSpeedCameraDict, SummaryStatisticDict
from src.database.connection import MySQLConnectionManager, with_db_connection
from src.domain.entity import Driver, Offense, Violation, SpeedCamera, Entity
from mysql.connector.connection import MySQLCursor, MySQLConnection
from typing import Type, cast
import inflection


class CrudRepository[T: Entity]:
    """Generic repository providing basic CRUD operations for entities.

    This class defines reusable methods for interacting with MySQL tables
    that correspond to entities in the domain model.

    Attributes:
        _connection_manager (MySQLConnectionManager): Manages pooled database connections.
        _entity_type (Type[T]): Entity class handled by the repository (e.g., `Driver`, `Offense`).
        _cursor (MySQLCursor): Active database cursor for query execution.
        _conn (MySQLConnection): Active MySQL connection object.
    """

    def __init__(self, connection_manager: MySQLConnectionManager, entity_type: Type[T]):
        self._connection_manager = connection_manager
        self._entity_type = entity_type
        self._cursor: MySQLCursor
        self._conn: MySQLConnection

    @with_db_connection
    def find_all(self) -> list[T]:
        """Retrieves all records from the entity's corresponding database table.

        Returns:
            list[T]: A list of entity instances. Returns an empty list if no records exist.
        """
        sql = f"select * from {self._table_name()}"
        self._cursor.execute(sql)

        if not self._cursor.description:
            return []  # pragma: no cover

        columns = [desc[0] for desc in self._cursor.description]
        rows = self._cursor.fetchall()
        if not rows:
            return []

        return [self._entity_type.from_row(self._convert_row_to_dict(columns, row)) for row in rows]

    @with_db_connection
    def find_by_id(self, item_id: int) -> T | None:
        """Finds a single record by its primary key ID.

        Args:
            item_id (int): Identifier of the entity to retrieve.

        Returns:
            T | None: The matching entity instance or None if not found.
        """
        sql = f'select * from {self._table_name()} where id_ = {item_id}'
        self._cursor.execute(sql)

        if not self._cursor.description:
            return None  # pragma: no cover

        item = self._cursor.fetchone()
        if item:
            columns = [desc[0] for desc in self._cursor.description]
            return self._entity_type.from_row(self._convert_row_to_dict(columns, item))
        return None

    @with_db_connection
    def insert(self, item: T) -> int | None:
        """Inserts a single entity record into the database.

        Args:
            item (T): Entity instance to be persisted.

        Returns:
            int | None: The ID of the newly inserted record, if available.
        """
        sql = (f'insert into {self._table_name()} '
               f'({self._column_names_for_insert()}) '
               f'values ({self._column_values_for_insert(item)})')
        self._cursor.execute(sql)
        return self._cursor.lastrowid

    @with_db_connection
    def insert_many(self, items: list[T]) -> None:
        """Inserts multiple records into the database in a single query.

        Args:
            items (list[T]): List of entity instances to insert.
        """
        if not items:
            return

        sql = (f'insert into {self._table_name()} ({self._column_names_for_insert()}) '
               f'values {", ".join(self._values_for_insert_many(items))}')
        self._cursor.execute(sql)

    @with_db_connection
    def update(self, item_id: int, item: T) -> None:
        """Updates an existing record in the database.

        Args:
            item_id (int): ID of the record to update.
            item (T): Entity instance with new field values.
        """
        sql = f'update {self._table_name()} set {self._column_names_and_values_for_update(item)} where id_ = {item_id}'
        self._cursor.execute(sql)

    @with_db_connection
    def delete(self, item_id: int) -> int:
        """Deletes a record from the database by ID.

        Args:
            item_id (int): ID of the entity to delete.

        Returns:
            int: The ID of the deleted record.
        """
        sql = f'delete from {self._table_name()} where id_ = {item_id}'
        self._cursor.execute(sql)
        return item_id

    def _table_name(self) -> str:
        """Infers the table name based on the entity class name.

        Returns:
            str: Table name (pluralized, snake_case version of the entity name).
        """
        return inflection.pluralize(inflection.underscore(self._entity_type.__name__))

    def _column_names_for_insert(self) -> str:
        """Builds a comma-separated list of column names for an INSERT query.

        Returns:
            str: SQL-compatible list of column names (excluding `id_`).
        """
        return ', '.join([field for field in self._entity_type.__annotations__.keys() if field != 'id_'])

    def _column_values_for_insert(self, item: T) -> str:
        """Builds a comma-separated list of column values for an INSERT query.

        Args:
            item (T): Entity instance providing the data.

        Returns:
            str: SQL-compatible string of values for insertion.
        """
        fields = [field for field in self._entity_type.__annotations__.keys() if field != 'id_']
        values = [
            str(getattr(item, field)) if isinstance(getattr(item, field), (int, float))
            else f"'{getattr(item, field)}'"
            for field in fields
        ]
        return ', '.join(values)

    def _column_names_and_values_for_update(self, item: T) -> str:
        """Creates a SQL-compatible `SET` clause for an UPDATE query.

        Args:
            item (T): Entity instance with new values.

        Returns:
            str: SQL string with column-value assignments.
        """
        return ', '.join([
            f"{field} = {str(getattr(item, field)) if isinstance(getattr(item, field), (int, float))
            else f"'{getattr(item, field)}'"}"
            for field in self._entity_type.__annotations__.keys()
            if field != 'id_'
        ])

    def _values_for_insert_many(self, items: list[T]) -> list[str]:
        """Generates multiple value tuples for batch inserts.

        Args:
            items (list[T]): List of entities to insert.

        Returns:
            list[str]: SQL-formatted value tuples.
        """
        return [f"({self._column_values_for_insert(item)})" for item in items]

    @staticmethod
    def _convert_row_to_dict(columns: list[str], row: tuple) -> dict:
        """Converts a database row into a dictionary mapping columns to values.

        Args:
            columns (list[str]): Column names from cursor description.
            row (tuple): Row data from database.

        Returns:
            dict: Mapping of column names to corresponding row values.
        """
        return {columns[i]: row[i] for i in range(len(columns))}

    @with_db_connection
    def _execute_query(self, sql: str, params: tuple | None = None) -> list[dict]:
        """Executes a raw SQL query and returns results as dictionaries.

        Args:
            sql (str): SQL query string.
            params (tuple | None): Optional query parameters for safe execution.

        Returns:
            list[dict]: List of rows as dictionaries. Empty list if no results.
        """
        self._cursor.execute(sql, params or ())
        if not self._cursor.description:
            return []
        columns = [desc[0] for desc in self._cursor.description]

        rows = self._cursor.fetchall()
        if not rows:
            return []

        return [self._convert_row_to_dict(columns, row) for row in rows]


class DriverRepository(CrudRepository[Driver]):
    """Repository for managing `Driver` entities."""

    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, Driver)


class OffenseRepository(CrudRepository[Offense]):
    """Repository for managing `Offense` entities."""

    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, Offense)


class SpeedCameraRepository(CrudRepository[SpeedCamera]):
    """Repository for managing `SpeedCamera` entities."""

    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, SpeedCamera)


class ViolationRepository(CrudRepository[Violation]):
    """Repository for managing `Violation` entities and complex analytical queries."""

    def __init__(self, connection_manager: MySQLConnectionManager):
        super().__init__(connection_manager, Violation)

    def find_violations_with_offense_by_driver(self, registration_number: str | None) -> list[DriverOffensesDict]:
        """Fetches all offenses committed by a specific driver, including totals.

        Args:
            registration_number (str | None): Driver's registration number.

        Returns:
            list[DriverOffensesDict]: List of offenses with penalty summaries.
        """
        sql = """
              SELECT d.first_name, 
                     d.last_name, 
                     d.registration_number, 
                     v.id_ as  violation_id, 
                     o.description, 
                     o.penalty_points, 
                     o.fine_amount, 
                     SUM(o.penalty_points) OVER (PARTITION BY d.id_) AS total_points, SUM(o.fine_amount) OVER (PARTITION BY d.id_) AS total_amount
              FROM violations v
                       JOIN drivers d ON v.driver_id = d.id_
                       JOIN offenses o ON v.offense_id = o.id_
              WHERE d.registration_number = %s; 
              """
        return [cast(DriverOffensesDict, row) for row in self._execute_query(sql, (registration_number,))]

    def get_driver_points(self) -> list[TopDriverDict]:
        """Calculates total penalty points for each driver.

        Returns:
            list[TopDriverDict]: Drivers ordered by total penalty points (descending).
        """
        sql = """
              SELECT d.id_, d.first_name, d.last_name, sum(o.penalty_points) as total_points 
              FROM violations v 
                       JOIN offenses o ON v.offense_id = o.id_ 
                       JOIN drivers d ON v.driver_id = d.id_
              GROUP BY d.id_, d.first_name, d.last_name
              ORDER BY total_points DESC; 
              """
        return [cast(TopDriverDict, row) for row in self._execute_query(sql)]

    def get_most_popular_speed_camera(self) -> list[PopularSpeedCameraDict]:
        """Finds the most frequently triggered speed cameras.

        Returns:
            list[PopularSpeedCameraDict]: Cameras with violation counts, ordered by frequency.
        """
        sql = """
              SELECT 
                s.location, 
                count(v.speed_camera_id) as total_count
              FROM speed_cameras s
              LEFT JOIN violations v ON v.speed_camera_id = s.id_
              group by s.location, s.id_
              order by total_count desc; 
              """
        return [cast(PopularSpeedCameraDict, row) for row in self._execute_query(sql)]

    def summary_statistics(self) -> list[SummaryStatisticDict]:
        """Generates overall violation and offense statistics.

        Returns:
            list[SummaryStatisticDict]: Summary metrics including totals and averages.
        """
        sql = """
              SELECT 
                COUNT(v.driver_id)              as total_drivers, 
                count(v.offense_id)             as total_offenses, 
                sum(o.penalty_points)           as total_points, 
                round(avg(o.penalty_points), 2) as average_points, 
                sum(o.fine_amount)              as total_fine_amount, 
                max(o.fine_amount)              as max_fine_amount, 
                min(o.fine_amount)              as min_fine_amount

                from violations v
                JOIN offenses o ON v.offense_id = o.id_ 
              """
        return [cast(SummaryStatisticDict, row) for row in self._execute_query(sql)]