from src.domain.repository import (
    DriverRepository,
    SpeedCameraRepository,
    OffenseRepository,
    ViolationRepository,
)
from src.service.dto import (
    DriverOffensesDto,
    TopDriverDto,
    PopularSpeedCameraDto,
    SummaryStatisticDto,
)
from src.config import logger


class ViolationService:
    """Service layer for handling operations related to traffic violations.

    This class provides high-level methods for retrieving and transforming
    violation-related data from various repositories. It coordinates data
    access and converts database query results into DTO objects for use in
    application logic or presentation layers.

    Attributes:
        driver_repository (DriverRepository): Repository for accessing driver data.
        speed_camera_repository (SpeedCameraRepository): Repository for accessing speed camera data.
        offense_repository (OffenseRepository): Repository for accessing offense data.
        violation_repository (ViolationRepository): Repository for accessing violation data.
    """

    def __init__(
        self,
        driver_repository: DriverRepository,
        speed_camera_repository: SpeedCameraRepository,
        offense_repository: OffenseRepository,
        violation_repository: ViolationRepository
    ):
        """Initialize the ViolationService with repository dependencies.

        Args:
            driver_repository (DriverRepository): Repository for driver data.
            speed_camera_repository (SpeedCameraRepository): Repository for speed camera data.
            offense_repository (OffenseRepository): Repository for offense data.
            violation_repository (ViolationRepository): Repository for violation data.
        """
        self.driver_repository = driver_repository
        self.speed_camera_repository = speed_camera_repository
        self.offense_repository = offense_repository
        self.violation_repository = violation_repository

    def get_offenses_by_driver(self, driver_number_registration: str) -> list[DriverOffensesDto]:
        """Retrieve all offenses committed by a specific driver.

        Fetches violation and offense data for a given driver registration number
        and returns them as a list of `DriverOffensesDto` objects.

        Args:
            driver_number_registration (str): The registration number of the driver.

        Returns:
            list[DriverOffensesDto]: A list of offenses associated with the driver.
        """
        result: list[DriverOffensesDto] = []
        violation = self.violation_repository.find_violations_with_offense_by_driver(driver_number_registration)
        if not violation:
            logger.info(f'Driver {driver_number_registration} has no violations')
        for v in violation:
            result.append(DriverOffensesDto.from_row(v))

        return result

    def get_top_drivers_by_points(self) -> list[TopDriverDto]:
        """Retrieve a ranking of drivers based on accumulated penalty points.

        Returns a list of drivers sorted by their total penalty points in
        descending order.

        Returns:
            list[TopDriverDto]: A list of top drivers with their total points.
        """
        violation = self.violation_repository.get_driver_points()
        result: list[TopDriverDto] = []
        if not violation:
            logger.info('No driver points')
        for v in violation:
            result.append(TopDriverDto.from_row(v))
        return result

    def get_speed_camera_statistic(self) -> list[PopularSpeedCameraDto]:
        """Retrieve statistics about the most frequently triggered speed cameras.

        Returns a list of speed cameras and the number of violations recorded by each.

        Returns:
            list[PopularSpeedCameraDto]: A list of speed cameras with violation counts.
        """
        result = []
        violation = self.violation_repository.get_most_popular_speed_camera()
        if not violation:
            logger.info(f'Speed camera has no violations')

        for v in violation:
            result.append(PopularSpeedCameraDto.from_row(v))

        return result

    def get_generate_report(self) -> list[SummaryStatisticDto]:
        """Generate a summary report of all recorded traffic violations.

        Aggregates statistics such as total drivers, offenses, penalty points,
        and fine amounts.

        Returns:
            list[SummaryStatisticDto]: A list containing summarized violation statistics.
        """
        result: list[SummaryStatisticDto] = []
        violation = self.violation_repository.summary_statistics()

        for v in violation:
            result.append(SummaryStatisticDto.from_row(v))
        return result