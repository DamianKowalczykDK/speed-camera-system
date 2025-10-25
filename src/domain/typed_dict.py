from typing import TypedDict
from datetime import date


class DriverDict(TypedDict, total=False):
    """Dictionary representation of a `Driver` entity.

    Attributes:
        id_ (int): Unique identifier of the driver.
        first_name (str): Driver's first name.
        last_name (str): Driver's last name.
        registration_number (str): Vehicle registration number assigned to the driver.
    """
    id_: int
    first_name: str
    last_name: str
    registration_number: str


class SpeedCameraDict(TypedDict, total=False):
    """Dictionary representation of a `SpeedCamera` entity.

    Attributes:
        id_ (int): Unique identifier of the speed camera.
        location (str): Physical location or description of the camera placement.
        allowed_speed (int): Maximum legal speed (km/h) monitored by the camera.
    """
    id_: int
    location: str
    allowed_speed: int


class OffenseDict(TypedDict, total=False):
    """Dictionary representation of an `Offense` entity.

    Attributes:
        id_ (int): Unique identifier of the offense.
        description (str): Text description of the traffic violation type.
        penalty_points (int): Number of penalty points assigned for the offense.
        fine_amount (int): Monetary fine amount associated with the offense.
    """
    id_: int
    description: str
    penalty_points: int
    fine_amount: int


class ViolationDict(TypedDict, total=False):
    """Dictionary representation of a `Violation` entity.

    Attributes:
        id_ (int): Unique identifier of the violation.
        violation_date (date): Date when the violation occurred.
        driver_id (int): ID of the driver responsible for the violation.
        speed_camera_id (int): ID of the speed camera that recorded the violation.
        offense_id (int): ID of the offense associated with the violation.
    """
    id_: int
    violation_date: date
    driver_id: int
    speed_camera_id: int
    offense_id: int


class DriverOffensesDict(TypedDict, total=False):
    """Aggregated data representing offenses committed by a single driver.

    Attributes:
        first_name (str): Driver's first name.
        last_name (str): Driver's last name.
        registration_number (str): Vehicle registration number.
        description (str): Description of the offense.
        penalty_points (int): Points assigned for this offense.
        fine_amount (int): Fine amount for this offense.
        total_points (int): Total penalty points accumulated by the driver.
        total_amount (int): Total fine amount accumulated by the driver.
    """
    first_name: str
    last_name: str
    registration_number: str
    description: str
    penalty_points: int
    fine_amount: int
    total_points: int
    total_amount: int


class SummaryStatisticDict(TypedDict, total=False):
    """Summary of system-wide traffic violation statistics.

    Attributes:
        total_drivers (int): Total number of drivers involved in violations.
        total_offenses (int): Total number of recorded offenses.
        total_points (int): Total sum of all penalty points.
        average_points (float): Average penalty points per violation.
        total_fine_amount (int): Sum of all fine amounts.
        max_fine_amount (int): Maximum fine value among all offenses.
        min_fine_amount (int): Minimum fine value among all offenses.
    """
    total_drivers: int
    total_offenses: int
    total_points: int
    average_points: float
    total_fine_amount: int
    max_fine_amount: int
    min_fine_amount: int


class TopDriverDict(TypedDict, total=False):
    """Representation of a driver ranked by total penalty points.

    Attributes:
        first_name (str): Driver's first name.
        last_name (str): Driver's last name.
        total_points (int): Total accumulated penalty points.
    """
    first_name: str
    last_name: str
    total_points: int


class PopularSpeedCameraDict(TypedDict, total=False):
    """Representation of a speed camera ranked by number of recorded violations.

    Attributes:
        location (str): Speed camera location.
        total_count (int): Total number of violations recorded by the camera.
    """
    location: str
    total_count: int