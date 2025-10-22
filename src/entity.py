from src.typed_dict import SpeedCameraDict, DriverDict, OffenseDict, ViolationDict, DriverOffensesDict, \
    SummaryStatisticDict, TopDriverDict, PopularSpeedCameraDict
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
            violation_date=row["violation_date"].isoformat() if row["violation_date"] else None,
            driver_id=row["driver_id"],
            speed_camera_id=row["speed_camera_id"],
            offense_id=row["offense_id"],
        )

@dataclass
class DriverOffenses:
    first_name: str | None = None
    last_name: str | None = None
    description: str | None = None
    penalty_points: int | None = None
    fine_amount: int | None = None
    total_points: int | None = None
    total_amount: int | None = None

    @classmethod
    def from_row(cls, row: DriverOffensesDict) -> Self:
        return cls(
            first_name=row["first_name"],
            last_name=row["last_name"],
            description=row["description"],
            penalty_points=row["penalty_points"],
            fine_amount=row["fine_amount"],
            total_points=row["total_points"],
            total_amount=row["total_amount"],
        )

@dataclass
class SummaryStatistic:
    total_drivers: int | None = None
    total_offenses: int | None = None
    total_points: int | None = None
    average_points: float | None = None
    total_fine_amount: int | None = None
    max_fine_amount: int | None = None
    min_fine_amount: int | None = None

    @classmethod
    def from_row(cls, row: SummaryStatisticDict) -> Self:
        return cls(
            total_drivers=row["total_drivers"],
            total_offenses=row["total_offenses"],
            total_points=row["total_points"],
            average_points=row["average_points"],
            total_fine_amount=row["total_fine_amount"],
            max_fine_amount=row["max_fine_amount"],
            min_fine_amount=row["min_fine_amount"],
        )


@dataclass
class TopDriver:
    first_name: str | None = None
    last_name: str | None = None
    total_points: int | None = None

    @classmethod
    def from_row(cls, row: TopDriverDict) -> Self:
        return cls(
            first_name=row["first_name"],
            last_name=row["last_name"],
            total_points=row["total_points"],
        )

@dataclass
class PopularSpeedCamera:
    location: str | None = None
    total_count: int | None = None

    @classmethod
    def from_row(cls, row: PopularSpeedCameraDict) -> Self:
        return cls(
            location=row["location"],
            total_count=row["total_count"],
        )