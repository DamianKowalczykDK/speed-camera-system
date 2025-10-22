from typing import cast
from unittest.mock import MagicMock, patch

import pytest

from src.domain.repository import DriverRepository, OffenseRepository, SpeedCameraRepository, ViolationRepository
from src.domain.typed_dict import PopularSpeedCameraDict
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
def popular_speed_camera_data_dict_1() -> PopularSpeedCameraDict:
    return {
        "location": 'Warshaw',
        "total_count": 5
    }

@pytest.fixture
def popular_speed_camera_data_dict_2() -> PopularSpeedCameraDict:
    return {
        "location": 'Krakow',
        "total_count": 3
    }

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

@patch('builtins.print')
def test_get_speed_camera_statistic_if_not_data(
    mock_print: MagicMock,
    mock_violation_repository: MagicMock,
    mock_violation_service: ViolationService
) -> None:
    mock_violation_repository.get_most_popular_speed_camera.return_value = []

    result = mock_violation_service.get_speed_camera_statistic()
    assert len(result) == 0
    mock_print.assert_called_once_with('Speed camera has no violations')


