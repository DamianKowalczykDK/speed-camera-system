from datetime import date, datetime

from src.domain.typed_dict import SpeedCameraDict, DriverDict, OffenseDict, ViolationDict
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, override


@dataclass
class Entity[T](ABC):
    id_: int | None = None

    @classmethod
    @abstractmethod
    def from_row(cls, row: T) -> Self: # pragma: no cover
        pass


@dataclass
class SpeedCamera(Entity[SpeedCameraDict]):
    location: str | None = None
    allowed_speed: int | None = None

    @classmethod
    @override
    def from_row(cls, row: SpeedCameraDict) -> Self:
        return cls(
            id_=row["id_"],
            location=row["location"],
            allowed_speed=row["allowed_speed"],
        )

@dataclass
class Driver(Entity[DriverDict]):
    first_name: str | None = None
    last_name: str | None = None
    registration_number: str | None = None

    @classmethod
    @override
    def from_row(cls, row: DriverDict) -> Self:
        return cls(
            id_=row["id_"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            registration_number=row["registration_number"],
        )

@dataclass
class Offense(Entity[OffenseDict]):
    description: str | None = None
    penalty_points: int | None = None
    fine_amount: int | None = None

    @classmethod
    @override
    def from_row(cls, row: OffenseDict) -> Self:
        return cls(
            id_=row["id_"],
            description=row["description"],
            penalty_points=row["penalty_points"],
            fine_amount=row["fine_amount"],
        )


@dataclass
class Violation(Entity[ViolationDict]):
    violation_date: str | None = None
    driver_id: int | None = None
    speed_camera_id: int | None = None
    offense_id: int | None = None

    @classmethod
    @override
    def from_row(cls, row: ViolationDict) -> Self:
        return cls(
            id_=row["id_"],
            violation_date=row["violation_date"].isoformat() if "violation_date" in row else None,
            driver_id=row["driver_id"],
            speed_camera_id=row["speed_camera_id"],
            offense_id=row["offense_id"],
        )
