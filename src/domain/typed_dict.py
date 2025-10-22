from typing import TypedDict
from datetime import date

class DriverDict(TypedDict, total=False):
    id_: int
    first_name: str
    last_name: str
    registration_number: str


class SpeedCameraDict(TypedDict, total=False):
    id_: int
    location: str
    allowed_speed: int


class OffenseDict(TypedDict, total=False):
    id_: int
    description: str
    penalty_points: int
    fine_amount: int


class ViolationDict(TypedDict, total=False):
    id_: int
    violation_date: date
    driver_id: int
    speed_camera_id: int
    offense_id: int

class DriverOffensesDict(TypedDict, total=False):
    first_name: str
    last_name: str
    registration_number: str
    description: str
    penalty_points: int
    fine_amount: int
    total_points: int
    total_amount: int

class SummaryStatisticDict(TypedDict, total=False):
    total_drivers: int
    total_offenses: int
    total_points: int
    average_points: float
    total_fine_amount: int
    max_fine_amount: int
    min_fine_amount: int

class TopDriverDict(TypedDict, total=False):
    first_name: str
    last_name: str
    total_points: int

class PopularSpeedCameraDict(TypedDict, total=False):
    location: str
    total_count: int

