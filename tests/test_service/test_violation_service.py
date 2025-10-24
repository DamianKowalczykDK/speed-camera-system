from src.domain.typed_dict import PopularSpeedCameraDict, TopDriverDict, DriverOffensesDict, SummaryStatisticDict
from src.service.violation_service import ViolationService
from unittest.mock import MagicMock
import logging
import pytest

def test_get_speed_camera_statistic_returns_data(
        mock_violation_repository: MagicMock,
        mock_violation_service: ViolationService,
        popular_speed_camera_data_dict_1: PopularSpeedCameraDict,
        popular_speed_camera_data_dict_2: PopularSpeedCameraDict
) -> None:
    mock_violation_repository.get_most_popular_speed_camera.return_value = [
        popular_speed_camera_data_dict_1, popular_speed_camera_data_dict_2
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
        top_driver_data_dict_1: TopDriverDict
) -> None:
    mock_violation_repository.get_driver_points.return_value = [top_driver_data_dict_1]
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



