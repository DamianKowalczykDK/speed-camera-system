from src.domain.repository import DriverRepository, OffenseRepository, SpeedCameraRepository, ViolationRepository
from src.service.violation_service import ViolationService
from unittest.mock import MagicMock
import pytest

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
