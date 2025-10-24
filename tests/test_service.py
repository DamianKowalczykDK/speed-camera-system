import logging
from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from src.domain.repository import DriverRepository, OffenseRepository, SpeedCameraRepository, ViolationRepository
from src.domain.typed_dict import PopularSpeedCameraDict, TopDriverDict, DriverOffensesDict, SummaryStatisticDict, \
    SpeedCameraDict
from src.service.dto import PopularSpeedCameraDto
from src.service.violation_service import ViolationService


@pytest.fixture
def mock_driver_repository() -> MagicMock:
    return MagicMock(spec=DriverRepository)
@pytest.fixture
def mock_offense_repository() -> MagicMock:
    return MagicMock(spec=OffenseRepository)
@pytest.fixture
def mock_speed_camera_repository() -> MagicMock:
    return MagicMock(spec=SpeedCameraRepository)
@pytest.fixture
def mock_violation_repository() -> MagicMock:
    return MagicMock(spec=ViolationRepository)

@pytest.fixture
def mock_violation_service(
        mock_driver_repository: MagicMock,
        mock_offense_repository: MagicMock,
        mock_speed_camera_repository: MagicMock,
        mock_violation_repository: MagicMock
) -> ViolationService:
    return ViolationService(
        driver_repository=mock_driver_repository,
        offense_repository=mock_offense_repository,
        speed_camera_repository=mock_speed_camera_repository,
        violation_repository=mock_violation_repository
    )

@pytest.fixture
def speed_camera_data_dict_1() -> PopularSpeedCameraDict:
    return {
        "location": 'Warshaw',
        "total_count": 5
    }

@pytest.fixture
def speed_camera_data_dict_2() -> PopularSpeedCameraDict:
    return {
        "location": 'Krakow',
        "total_count": 3
    }

@pytest.fixture
def driver_data_dict_1() -> TopDriverDict:
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'total_points': 7
    }

@pytest.fixture
def driver_offense_data_dict_1() -> DriverOffensesDict:
    return {
        'first_name': 'John',
        'last_name': 'Doe',
        'description': 'Test',
        'penalty_points': 1,
        'fine_amount': 100,
        'total_points': 1,
        'total_amount': 1
    }

@pytest.fixture
def summary_statistics_data_dict_1() -> SummaryStatisticDict:
    return {
        'total_drivers': 4,
        'total_offenses': 4,
        'total_points': 9,
        'average_points': 2.25,
        'total_fine_amount': 300,
        'max_fine_amount': 200,
        'min_fine_amount': 100,
    }

def test_get_speed_camera_statistic_returns_data(
        mock_violation_repository: MagicMock,
        mock_violation_service: ViolationService,
        speed_camera_data_dict_1: PopularSpeedCameraDict,
        speed_camera_data_dict_2: PopularSpeedCameraDict
) -> None:
    mock_violation_repository.get_most_popular_speed_camera.return_value = [
        speed_camera_data_dict_1, speed_camera_data_dict_2
    ]
    result = mock_violation_service.get_speed_camera_statistic()
    assert len(result) == 2
    assert result[0].location == 'Warshaw'
    assert result[0].total_count == 5
    assert result[1].location == "Krakow"
    assert result[1].total_count == 3
    mock_violation_repository.get_most_popular_speed_camera.assert_called_once()


def test_get_speed_camera_statistic_if_not_data(
    mock_violation_repository: MagicMock,
    mock_violation_service: ViolationService,
    caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_violation_repository.get_most_popular_speed_camera.return_value = []
        result = mock_violation_service.get_speed_camera_statistic()
    assert len(result) == 0
    assert 'Speed camera has no violations' in caplog.text


def test_get_top_drivers_by_point_returns_data(
        mock_violation_repository: MagicMock,
        mock_violation_service: ViolationService,
        driver_data_dict_1: TopDriverDict
) -> None:
    mock_violation_repository.get_driver_points.return_value = [driver_data_dict_1]
    result = mock_violation_service.get_top_drivers_by_points()
    assert len(result) == 1

    assert result[0].first_name == 'John'
    assert result[0].last_name == 'Doe'
    assert result[0].total_points == 7

def test_get_top_drivers_by_point_if_not_data(
    mock_violation_repository: MagicMock,
    mock_violation_service: ViolationService,
    caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_violation_repository.get_driver_points.return_value = []
        result = mock_violation_service.get_top_drivers_by_points()
    assert len(result) == 0
    assert 'No driver points' in caplog.text

def test_get_offenses_by_driver_returns_data(
        mock_violation_repository: MagicMock,
        mock_violation_service: ViolationService,
        driver_offense_data_dict_1: DriverOffensesDict
) -> None:
    mock_violation_repository.find_violations_with_offense_by_driver.return_value = [driver_offense_data_dict_1]
    result = mock_violation_service.get_offenses_by_driver('K123456')
    assert len(result) == 1

    assert result[0].first_name == 'John'
    assert result[0].last_name == 'Doe'
    assert result[0].description == 'Test'
    assert result[0].total_points == 1

def test_get_offenses_by_driver_if_not_data(
        mock_violation_repository: MagicMock,
        mock_violation_service: ViolationService,
        caplog: pytest.LogCaptureFixture
) -> None:
    with caplog.at_level(logging.INFO):
        mock_violation_repository.find_violations_with_offense_by_driver.return_value = []
        result = mock_violation_service.get_offenses_by_driver('K123456')
    assert len(result) == 0
    assert 'Driver K123456 has no violations' in caplog.text


def test_get_generate_report(
        mock_violation_repository: MagicMock,
        mock_violation_service: ViolationService,
        summary_statistics_data_dict_1: SummaryStatisticDict
) -> None:
    mock_violation_repository.summary_statistics.return_value = [summary_statistics_data_dict_1]
    result = mock_violation_service.get_generate_report()
    assert len(result) == 1

    assert result[0].total_fine_amount == 300
    assert result[0].total_drivers == 4
    assert result[0].total_offenses == 4
    assert result[0].total_points == 9



