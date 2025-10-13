from dataclasses import dataclass
from abc import ABC, abstractmethod
from typing import Self, override


@dataclass
class Entity(ABC):
    id_: int | None = None

    @classmethod
    @abstractmethod
    def from_row(cls, *args: str) -> Self: # pragma: no cover
        pass


@dataclass
class SpeedCamera(Entity):
    location: str | None = None
    allowed_speed: int | None = None

    @classmethod
    @override
    def from_row(cls, *args: str) -> Self:
        return cls(
            id_=int(args[0]),
            location=str(args[1]),
            allowed_speed=int(args[2]),
        )


@dataclass
class Driver(Entity):
    first_name: str | None = None
    last_name: str | None = None
    registration_number: str | None = None

    @classmethod
    @override
    def from_row(cls, *args: str) -> Self:
        return cls(
            id_=int(args[0]),
            first_name=str(args[1]),
            last_name=str(args[2]),
            registration_number=str(args[3])
        )


@dataclass
class Offense(Entity):
    description: str | None = None
    penalty_points: int | None = None
    fine_amount: int | None = None

    @classmethod
    @override
    def from_row(cls, *args: str) -> Self:
        return cls(
            id_=int(args[0]),
            description=str(args[1]),
            penalty_points=int(args[2]),
            fine_amount=int(args[3]),
        )


@dataclass
class Violation(Entity):
    violation_date: str | None = None
    driver_id: int | None = None
    speed_camera_id: int | None = None
    offense_id: int | None = None

    @classmethod
    @override
    def from_row(cls, *args: str) -> Self:
        return cls(
            id_=int(args[0]),
            violation_date=str(args[1]),
            driver_id=int(args[2]),
            speed_camera_id=int(args[3]),
            offense_id=int(args[4]),
        )