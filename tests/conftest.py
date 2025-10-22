from typing import Generator

from src.entity import Driver, SpeedCamera, Offense
from src.repository import DriverRepository, SpeedCameraRepository, ViolationRepository, OffenseRepository
from src.execute_sql_file import SqlFileExecutor
from testcontainers.mysql import MySqlContainer
from src.database import MySQLConnectionManager
from urllib.parse import urlparse
import pytest
import os

@pytest.fixture
def driver_1() -> Driver:
    return Driver(id_=1, first_name='Jon', last_name='Smith', registration_number='ABC123')
@pytest.fixture
def driver_2() -> Driver:
    return Driver(id_=2, first_name='Bob', last_name='Doe', registration_number='XYZ123')

@pytest.fixture
def speed_camera_1() -> SpeedCamera:
    return SpeedCamera(id_=1,location='Warsaw', allowed_speed=50)

@pytest.fixture
def speed_camera_2() -> SpeedCamera:
    return SpeedCamera(id_=2, location='Krakow', allowed_speed=70)

@pytest.fixture
def offense_1() -> Offense:
    return Offense(id_=1, description='Test', penalty_points=2, fine_amount=200)

@pytest.fixture(scope='module')
def mysql_container() -> Generator[MySqlContainer]:
    with MySqlContainer('mysql:latest') as container:
        yield container

@pytest.fixture(scope='module')
def connection_manager(mysql_container: MySqlContainer) -> MySQLConnectionManager:
    connection_url = mysql_container.get_connection_url()
    parsed_url = urlparse(connection_url)

    os.environ['DB_HOST'] = parsed_url.hostname
    os.environ['DB_PORT'] = str(parsed_url.port)
    os.environ['DB_USERNAME'] = parsed_url.username
    os.environ['DB_PASSWORD'] = parsed_url.password
    os.environ['DB_NAME'] = parsed_url.path[1:]
    os.environ['DB_POOL_SIZE'] = '5'
    return MySQLConnectionManager()

@pytest.fixture(scope='module', autouse=True)
def setup_database_schema(connection_manager: MySQLConnectionManager) -> None:
    execute_sql = SqlFileExecutor(connection_manager)
    execute_sql.execute_sql_file(os.path.join(os.path.dirname(__file__), '../sql/schema.sql'))

@pytest.fixture
def driver_repository(connection_manager: MySQLConnectionManager) -> DriverRepository:
    return DriverRepository(connection_manager)

@pytest.fixture
def speed_camera_repository(connection_manager: MySQLConnectionManager) -> SpeedCameraRepository:
    return SpeedCameraRepository(connection_manager)

@pytest.fixture
def violation_repository(connection_manager: MySQLConnectionManager) -> ViolationRepository:
    return ViolationRepository(connection_manager)

@pytest.fixture
def offense_repository(connection_manager: MySQLConnectionManager) -> OffenseRepository:
    return OffenseRepository(connection_manager)

@pytest.fixture
def clear_database(connection_manager: MySQLConnectionManager) -> None:
    with connection_manager.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()

        for (table_name,) in tables:
            table_name_str = table_name.decode() if isinstance(table_name, bytes) else table_name
            cursor.execute(f"TRUNCATE TABLE {table_name_str};")

        cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")
        conn.commit()