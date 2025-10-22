from src.entity import DriverOffenses, SummaryStatistic, TopDriver, PopularSpeedCamera
from src.repository import DriverRepository, SpeedCameraRepository, OffenseRepository, ViolationRepository
from tests.conftest import violation_repository


class ViolationService:
    def __init__(
            self,
            driver_repository: DriverRepository,
            speed_camera_repository: SpeedCameraRepository,
            offense_repository: OffenseRepository,
            violation_repository: ViolationRepository
    ):
        self.driver_repository = driver_repository
        self.speed_camera_repository = speed_camera_repository
        self.offense_repository = offense_repository
        self.violation_repository = violation_repository


    def get_offenses_by_driver(self, driver_number_registration: str) -> list[DriverOffenses]:
        result: list[DriverOffenses] = []
        violation = self.violation_repository.find_violations_with_offense_by_driver(driver_number_registration)
        if not violation:
            print(f'Driver {driver_number_registration} has no violations')
        for v in violation:
            result.append(DriverOffenses.from_row(v))

        return result


    def get_top_drivers_by_points(self) -> list[TopDriver]:
        violation = self.violation_repository.get_driver_points()
        result: list[TopDriver] = []
        if not violation:
            print(f'No driver points')
        for v in violation:
            result.append(TopDriver.from_row(v))
        return result


    def get_speed_camera_statistic(self) -> list[PopularSpeedCamera]:
        result = []
        violation = self.violation_repository.get_most_popular_speed_camera()
        if not violation:
            print(f'Speed camera has no violations')

        for v in violation:
            result.append(PopularSpeedCamera.from_row(v))

        return result

    def get_generate_report(self) -> list[SummaryStatistic]:
        result: list[SummaryStatistic] = []
        violation = self.violation_repository.summary_statistics()

        for v in violation:
            result.append(SummaryStatistic.from_row(v))
        return result


