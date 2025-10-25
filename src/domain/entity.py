from src.domain.typed_dict import SpeedCameraDict, DriverDict, OffenseDict, ViolationDict
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Self, override


@dataclass
class Entity[T](ABC):
    """Abstract base class for all domain entities.

    Provides a common structure for entities with an `id_` field and defines
    a factory method for creating entities from database rows or dictionaries.

    Type Args:
        T: A TypedDict representing the database row structure for the entity.
    """

    id_: int | None = None

    @classmethod
    @abstractmethod
    def from_row(cls, row: T) -> Self:  # pragma: no cover
        """Creates an entity instance from a database row or dictionary.

        Args:
            row (T): A dictionary (TypedDict) containing database record data.

        Returns:
            Self: An instance of the entity populated with data from the row.
        """
        pass


@dataclass
class SpeedCamera(Entity[SpeedCameraDict]):
    """Represents a speed camera record from the database.

    Attributes:
        id_ (int | None): Unique identifier of the speed camera.
        location (str | None): Location or name of the speed camera.
        allowed_speed (int | None): Maximum allowed speed (in km/h) for the location.
    """

    location: str | None = None
    allowed_speed: int | None = None

    @classmethod
    @override
    def from_row(cls, row: SpeedCameraDict) -> Self:
        """Creates a SpeedCamera entity from a dictionary row.

        Args:
            row (SpeedCameraDict): Dictionary containing speed camera data.

        Returns:
            SpeedCamera: Entity instance populated with the given row data.
        """
        return cls(
            id_=row["id_"],
            location=row["location"],
            allowed_speed=row["allowed_speed"],
        )


@dataclass
class Driver(Entity[DriverDict]):
    """Represents a driver record from the database.

    Attributes:
        id_ (int | None): Unique identifier of the driver.
        first_name (str | None): Driver's first name.
        last_name (str | None): Driver's last name.
        registration_number (str | None): Vehicle registration number assigned to the driver.
    """

    first_name: str | None = None
    last_name: str | None = None
    registration_number: str | None = None

    @classmethod
    @override
    def from_row(cls, row: DriverDict) -> Self:
        """Creates a Driver entity from a dictionary row.

        Args:
            row (DriverDict): Dictionary containing driver data.

        Returns:
            Driver: Entity instance populated with the given row data.
        """
        return cls(
            id_=row["id_"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            registration_number=row["registration_number"],
        )


@dataclass
class Offense(Entity[OffenseDict]):
    """Represents an offense record from the database.

    Attributes:
        id_ (int | None): Unique identifier of the offense.
        description (str | None): Description of the offense.
        penalty_points (int | None): Number of penalty points assigned for the offense.
        fine_amount (int | None): Monetary fine (in PLN) for the offense.
    """

    description: str | None = None
    penalty_points: int | None = None
    fine_amount: int | None = None

    @classmethod
    @override
    def from_row(cls, row: OffenseDict) -> Self:
        """Creates an Offense entity from a dictionary row.

        Args:
            row (OffenseDict): Dictionary containing offense data.

        Returns:
            Offense: Entity instance populated with the given row data.
        """
        return cls(
            id_=row["id_"],
            description=row["description"],
            penalty_points=row["penalty_points"],
            fine_amount=row["fine_amount"],
        )


@dataclass
class Violation(Entity[ViolationDict]):
    """Represents a traffic violation record from the database.

    Attributes:
        id_ (int | None): Unique identifier of the violation.
        violation_date (str | None): ISO 8601 formatted date of the violation.
        driver_id (int | None): ID of the driver involved in the violation.
        speed_camera_id (int | None): ID of the speed camera that recorded the violation.
        offense_id (int | None): ID of the related offense definition.
    """

    violation_date: str | None = None
    driver_id: int | None = None
    speed_camera_id: int | None = None
    offense_id: int | None = None

    @classmethod
    @override
    def from_row(cls, row: ViolationDict) -> Self:
        """Creates a Violation entity from a dictionary row.

        Args:
            row (ViolationDict): Dictionary containing violation data.

        Returns:
            Violation: Entity instance populated with the given row data.
        """
        return cls(
            id_=row["id_"],
            violation_date=row["violation_date"].isoformat() if "violation_date" in row else None,
            driver_id=row["driver_id"],
            speed_camera_id=row["speed_camera_id"],
            offense_id=row["offense_id"],
        )