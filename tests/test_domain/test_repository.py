from src.domain.repository import DriverRepository, SpeedCameraRepository, ViolationRepository, OffenseRepository
from src.domain.typed_dict import PopularSpeedCameraDict, TopDriverDict, SummaryStatisticDict, DriverOffensesDict
from src.domain.entity import Driver, SpeedCamera, Offense, Violation
from src.database.execute_sql_file import SqlFileExecutor
from src.database.connection import MySQLConnectionManager
from mysql.connector import Error
from unittest.mock import patch
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
        execute_sql.execute_sql_file(os.path.join(os.path.dirname(__file__), '../../sql/data_test.sql'))


def test_get_most_popular_speed_camera(
        mock_violation_repository_with_mocked_query: ViolationRepository,
        popular_speed_camera_data_dict_1: PopularSpeedCameraDict
) -> None:
    with patch.object(
            ViolationRepository,
            '_execute_query',
            return_value=[popular_speed_camera_data_dict_1]
    ) as mock_execute_query:

        result = mock_violation_repository_with_mocked_query.get_most_popular_speed_camera()
        assert mock_execute_query.call_count == 1
    assert result[0]['location'] == 'Warshaw'
    assert result[0]['total_count'] == 5

def test_get_driver_points(
        mock_violation_repository_with_mocked_query: ViolationRepository,
        top_driver_data_dict_1: TopDriverDict
) -> None:
    with patch.object(
            ViolationRepository,
            '_execute_query',
            return_value=[top_driver_data_dict_1]
    ) as mock_execute_query:
        result = mock_violation_repository_with_mocked_query.get_driver_points()
        assert mock_execute_query.call_count == 1

    assert result[0]['first_name'] == 'John'
    assert result[0]['last_name'] == 'Doe'
    assert result[0]['total_points'] == 7

def test_summary_statistics(
        mock_violation_repository_with_mocked_query: ViolationRepository,
        summary_statistics_data_dict_1: SummaryStatisticDict
) -> None:
    with patch.object(
            ViolationRepository,
            '_execute_query',
            return_value=[summary_statistics_data_dict_1]
    ) as mock_execute_query:
        result = mock_violation_repository_with_mocked_query.summary_statistics()
        assert mock_execute_query.call_count == 1
    assert result[0]['total_drivers'] == 4
    assert result[0]['total_offenses'] == 4
    assert result[0]['total_points'] == 9
    assert result[0]['average_points'] == 2.25
    assert result[0]['total_fine_amount'] == 300
    assert result[0]['max_fine_amount'] == 200
    assert result[0]['min_fine_amount'] == 100


def test_find_violations_with_offense_by_driver(
        mock_violation_repository_with_mocked_query: ViolationRepository,
        driver_offense_data_dict_1: DriverOffensesDict
) -> None:
    with patch.object(
            ViolationRepository,
            '_execute_query',
            return_value=[driver_offense_data_dict_1]
    ) as mock_execute_query:
        result = mock_violation_repository_with_mocked_query.find_violations_with_offense_by_driver('K123456')
        assert mock_execute_query.call_count == 1
    assert result[0]['first_name'] == 'John'
    assert result[0]['last_name'] == 'Doe'
    assert result[0]['description'] == 'Test'
    assert result[0]['penalty_points'] == 1
    assert result[0]['fine_amount'] == 100
    assert result[0]['total_points'] == 1
    assert result[0]['total_amount'] == 100

def test_execute_query(violation_repository: ViolationRepository) -> None:
    result = violation_repository._execute_query('SELECT * FROM speed_cameras')
    assert result is not None

def test_execute_query_if_not_data(violation_repository: ViolationRepository, clear_database) -> None:
     result = violation_repository._execute_query(
         "INSERT INTO speed_cameras (id_, location, allowed_speed) VALUES (1, 'Test', 50)"
     )
     assert result == []

def test_execute_query_return_data(
        speed_camera_repository: SpeedCameraRepository,
        violation_repository: ViolationRepository,
        speed_camera_1: SpeedCamera,
        clear_database
) -> None:

    speed_camera_repository.insert(speed_camera_1)
    result = violation_repository._execute_query(
        "SELECT location FROM speed_cameras WHERE id_ = 1"
    )
    assert result[0]['location'] == 'Warsaw'

