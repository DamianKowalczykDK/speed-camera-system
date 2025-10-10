from dataclasses import dataclass

@dataclass
class SpeedCamera:
    id_: int | None = None
    location: str | None = None
    allowed_speed: int | None = None

@dataclass
class Driver:
    id_: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    registration_number: str | None = None

@dataclass
class Offence:
    id_: int | None = None
    description: str | None = None
    penalty_points: int | None = None
    fine_amount: int | None = None

@dataclass
class Violation:
    id_: int | None = None
    violation_date: str | None = None
    driver_id: int | None = None
    speed_camera_id: int | None = None
    offence_id: int | None = None