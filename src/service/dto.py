from dataclasses import dataclass
from typing import Self
from src.domain.typed_dict import DriverOffensesDict, \
    SummaryStatisticDict, TopDriverDict, PopularSpeedCameraDict


@dataclass
class DriverOffensesDto:
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
class SummaryStatisticDto:
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
class TopDriverDto:
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
class PopularSpeedCameraDto:
    location: str | None = None
    total_count: int | None = None

    @classmethod
    def from_row(cls, row: PopularSpeedCameraDict) -> Self:
        return cls(
            location=row["location"],
            total_count=row["total_count"],
        )