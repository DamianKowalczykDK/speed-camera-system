from collections import Counter
from itertools import count

from src.entity import Driver, Offense
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

    def get_offenses_by_driver(self, driver_number_registration: str) -> str:
        total_points = 0
        total_amount = 0
        result = []
        driver = [d for d in self.driver_repository.find_all() if d.registration_number == driver_number_registration]
        if not driver:
            print(f'{driver_number_registration} is not registered')
        for d in driver:
            all_violations = self.violation_repository.find_all()
            violation_for_driver = [v for v in all_violations if v.driver_id == d.id_]
            for violation in violation_for_driver:
                offense = self.offense_repository.find_by_id(violation.offense_id)
                if offense:
                    total_points += offense.penalty_points
                    total_amount += offense.fine_amount

                    result.append(
                        f'Driver name: {d.first_name} {d.last_name}\n'
                        f'Description: {offense.description}\n'
                        f'points: {offense.penalty_points}\n'
                        f'fine amount: {offense.fine_amount}\n'
                        )
            result.append(f'Total points: {total_points}\nTotal amount: {total_amount}')

        return '\n'.join(result)

    def get_top_drivers_by_points(self) -> list[str]:
        result = []
        all_driver = self.driver_repository.find_all()
        driver_points: dict[int, int] = {d.id_: 0 for d in all_driver}
        all_violations = self.violation_repository.find_all()
        for violation in all_violations:
            offense = self.offense_repository.find_by_id(violation.offense_id)
            if offense:
                driver_points[violation.driver_id] += offense.penalty_points
        for driver in all_driver:
            total_points = driver_points.get(driver.id_, 0)
            if driver_points[driver.id_] > 0:
                result.append(f'Driver: {driver.first_name} {driver.last_name}, points: {total_points}')

        return sorted(result, reverse=True)

    def get_camera_violations(self) -> dict[str, int]:
        all_speed_cameras = self.speed_camera_repository.find_all()
        all_violations = self.violation_repository.find_all()
        best_speed_camera: dict[str, int] = {s.location: 0 for s in all_speed_cameras}

        counts = Counter(v.speed_camera_id for v in all_violations)
        for camera in all_speed_cameras:
            best_speed_camera[camera.location] += counts[camera.id_]
        return best_speed_camera

    def get_summary_statistic(self) -> str:
        driver_repository = self.driver_repository.find_all()
        offense_repository = self.offense_repository.find_all()
        count_all_drivers = len(driver_repository)
        count_all_offenses = len(offense_repository)
        avg_points = sum(
            o.penalty_points for o in offense_repository) / count_all_offenses if count_all_offenses > 0 else 0

        total_points = sum(o.penalty_points for o in offense_repository)
        total_fine_amount = sum(o.fine_amount for o in offense_repository)
        if offense_repository:
            max_fine_amount = max(o.fine_amount for o in offense_repository)
            min_fine_amount = min(o.fine_amount for o in offense_repository)
        else:
            max_fine_amount, min_fine_amount = 0, 0
        return (f''
                f'All drivers: {count_all_drivers}\nAll offenses: {count_all_offenses}\n'
                f'Total points: {total_points}\n'
                f'Average points: {round(avg_points, 2)}\nTotal fine_amount: {total_fine_amount}\n'
                f'Max fine amount: {max_fine_amount}\n'
                f'Min fine amount: {min_fine_amount}'
        )



