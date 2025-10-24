from src.domain.typed_dict import PopularSpeedCameraDict, TopDriverDict, DriverOffensesDict, SummaryStatisticDict
from src.domain.entity import Driver, SpeedCamera, Offense
import pytest


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

@pytest.fixture
def top_driver_data_dict_1() -> TopDriverDict:
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
        'total_amount': 100
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