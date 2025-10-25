from dataclasses import dataclass
from typing import Self
from src.domain.typed_dict import (
    DriverOffensesDict,
    SummaryStatisticDict,
    TopDriverDict,
    PopularSpeedCameraDict,
)


@dataclass
class DriverOffensesDto:
    """Data Transfer Object representing offenses committed by a specific driver.

    This DTO is used to transport aggregated information about all offenses
    committed by a driver, including their total penalty points and fines.

    Attributes:
        first_name (str | None): Driver's first name.
        last_name (str | None): Driver's last name.
        description (str | None): Description of the offense.
        penalty_points (int | None): Points assigned for this specific offense.
        fine_amount (int | None): Fine amount for this specific offense.
        total_points (int | None): Total points accumulated by the driver.
        total_amount (int | None): Total fine amount accumulated by the driver.
    """

    first_name: str | None = None
    last_name: str | None = None
    description: str | None = None
    penalty_points: int | None = None
    fine_amount: int | None = None
    total_points: int | None = None
    total_amount: int | None = None

    @classmethod
    def from_row(cls, row: DriverOffensesDict) -> Self:
        """Create a `DriverOffensesDto` from a database row.

        Args:
            row (DriverOffensesDict): Dictionary containing driver and offense data.

        Returns:
            Self: Instance of `DriverOffensesDto` populated with row data.
        """
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
    """Data Transfer Object representing summary statistics of all violations.

    Attributes:
        total_drivers (int | None): Total number of drivers involved in violations.
        total_offenses (int | None): Total number of offenses recorded.
        total_points (int | None): Total penalty points across all offenses.
        average_points (float | None): Average penalty points per offense.
        total_fine_amount (int | None): Total fine amount across all offenses.
        max_fine_amount (int | None): Highest fine amount recorded.
        min_fine_amount (int | None): Lowest fine amount recorded.
    """

    total_drivers: int | None = None
    total_offenses: int | None = None
    total_points: int | None = None
    average_points: float | None = None
    total_fine_amount: int | None = None
    max_fine_amount: int | None = None
    min_fine_amount: int | None = None

    @classmethod
    def from_row(cls, row: SummaryStatisticDict) -> Self:
        """Create a `SummaryStatisticDto` from a database row.

        Args:
            row (SummaryStatisticDict): Dictionary containing statistical data.

        Returns:
            Self: Instance of `SummaryStatisticDto` populated with row data.
        """
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
    """Data Transfer Object representing a driver ranked by penalty points.

    Attributes:
        first_name (str | None): Driver's first name.
        last_name (str | None): Driver's last name.
        total_points (int | None): Total penalty points accumulated by the driver.
    """

    first_name: str | None = None
    last_name: str | None = None
    total_points: int | None = None

    @classmethod
    def from_row(cls, row: TopDriverDict) -> Self:
        """Create a `TopDriverDto` from a database row.

        Args:
            row (TopDriverDict): Dictionary containing driver ranking data.

        Returns:
            Self: Instance of `TopDriverDto` populated with row data.
        """
        return cls(
            first_name=row["first_name"],
            last_name=row["last_name"],
            total_points=row["total_points"],
        )


@dataclass
class PopularSpeedCameraDto:
    """Data Transfer Object representing a speed camera and its usage frequency.

    Attributes:
        location (str | None): Location or description of the speed camera.
        total_count (int | None): Total number of violations recorded by this camera.
    """

    location: str | None = None
    total_count: int | None = None

    @classmethod
    def from_row(cls, row: PopularSpeedCameraDict) -> Self:
        """Create a `PopularSpeedCameraDto` from a database row.

        Args:
            row (PopularSpeedCameraDict): Dictionary containing camera usage data.

        Returns:
            Self: Instance of `PopularSpeedCameraDto` populated with row data.
        """
        return cls(
            location=row["location"],
            total_count=row["total_count"],
        )