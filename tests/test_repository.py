from src.repository import DriverRepository, SpeedCameraRepository, ViolationRepository, OffenseRepository
from src.entity import Driver, SpeedCamera, Offense, Violation
from src.execute_sql_file import SqlFileExecutor
from src.database import MySQLConnectionManager
from mysql.connector import Error
import pytest
import os


def test_insert_driver(driver_repository: DriverRepository, driver_1: Driver) -> None:
    driver_id = driver_repository.insert(driver_1)
    assert driver_id is not None

    retrieved_driver = driver_repository.find_by_id(1)
    assert retrieved_driver.first_name == driver_1.first_name
    assert retrieved_driver.last_name == driver_1.last_name
    assert retrieved_driver.registration_number == driver_1.registration_number

def test_insert_offense(offense_repository: OffenseRepository, offense_1: Offense) -> None:
    offense_id = offense_repository.insert(offense_1)
    assert offense_id is not None

    retrieved_offense = offense_repository.find_by_id(1)
    assert retrieved_offense.description == offense_1.description
    assert retrieved_offense.penalty_points == offense_1.penalty_points
    assert retrieved_offense.fine_amount == offense_1.fine_amount

def test_insert_driver_and_find_all(driver_repository: OffenseRepository, driver_1: Driver, clear_database) -> None:
    driver_id = driver_repository.insert(driver_1)
    assert driver_id is not None

    drivers_find_all = driver_repository.find_all()
    expected_offense = [driver_1]

    assert drivers_find_all == expected_offense

    retrieved_driver= driver_repository.find_by_id(1)
    assert retrieved_driver.first_name == driver_1.first_name
    assert retrieved_driver.last_name == driver_1.last_name
    assert retrieved_driver.registration_number == driver_1.registration_number


def test_insert_many_speed_camera(
        speed_camera_repository: SpeedCameraRepository,
        speed_camera_1: SpeedCamera,
        speed_camera_2: SpeedCamera
) -> None:
    speed_camera_repository.insert_many([speed_camera_1, speed_camera_2])

    retrieved_speed_camera_1 = speed_camera_repository.find_by_id(1)
    retrieved_speed_camera_2 = speed_camera_repository.find_by_id(2)
    assert retrieved_speed_camera_1.location == speed_camera_1.location
    assert retrieved_speed_camera_1.allowed_speed == speed_camera_1.allowed_speed
    assert retrieved_speed_camera_2.location == speed_camera_2.location
    assert retrieved_speed_camera_2.allowed_speed == speed_camera_2.allowed_speed

def test_insert_violation(
        driver_repository:DriverRepository,
        speed_camera_repository: SpeedCameraRepository,
        offense_repository: OffenseRepository,
        violation_repository: ViolationRepository,
        driver_1: Driver,
        speed_camera_1: SpeedCamera,
        offense_1: Offense
) -> None:
    driver_id = driver_repository.insert(driver_1)

    speed_camera_id = speed_camera_repository.insert(speed_camera_1)

    offense_id = offense_repository.insert(offense_1)

    expected_date = '2025-10-14'
    violation = Violation(
        violation_date=expected_date,
        driver_id=driver_id,
        speed_camera_id=speed_camera_id,
        offense_id=offense_id
    )

    violation_id = violation_repository.insert(violation)
    assert violation_id is not None

    retrieved_violation = violation_repository.find_by_id(violation_id)
    assert retrieved_violation.violation_date == expected_date
    assert retrieved_violation.driver_id == driver_id
    assert retrieved_violation.speed_camera_id == speed_camera_id
    assert retrieved_violation.offense_id == offense_id


def test_update_driver(driver_repository: DriverRepository, driver_1: Driver, driver_2: Driver) -> None:
    driver_id = driver_repository.insert(driver_1)
    updated_driver = driver_2

    driver_repository.update(driver_id, updated_driver)
    retrieved_driver = driver_repository.find_by_id(driver_id)
    assert retrieved_driver.first_name == updated_driver.first_name
    assert retrieved_driver.registration_number == updated_driver.registration_number

def test_delete_driver(driver_repository: DriverRepository, driver_1: Driver) -> None:
    driver_id = driver_repository.insert(driver_1)
    driver_repository.delete(driver_id)
    retrieved_driver = driver_repository.find_by_id(driver_id)
    assert retrieved_driver is None


def test_insert_many_if_not_rows(driver_repository: DriverRepository, clear_database) -> None:
    driver_repository.insert_many([])
    retrieved_driver = driver_repository.find_all()

    assert len(retrieved_driver) == 0


def test_with_db_connection_rollback(driver_repository: DriverRepository) -> None:
    with pytest.raises(Exception):
        driver_repository.insert()

def test_execute_sql_file(connection_manager: MySQLConnectionManager) -> None:
    execute_sql = SqlFileExecutor(connection_manager)
    with pytest.raises(Error):
        execute_sql.execute_sql_file(os.path.join(os.path.dirname(__file__), '../sql/data_test.sql'))


