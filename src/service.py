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

    def get_offenses_by_driver(self, driver_number_registration: str) -> str | None:
        total_points = 0
        total_amount = 0
        result = []
        violation = self.violation_repository.find_violations_with_offense_by_driver(driver_number_registration)
        if not violation:
            print(f'Driver {driver_number_registration} has no violations')
        for v in violation:
            result.append(f"Driver name: {v['first_name']} {v['last_name']}\n"
                          f"Description: {v['description']}\n"
                          f"Points: {v['penalty_points']}\n"
                          f"Amount: {v['fine_amount']}\n")
            total_points += v['penalty_points']
            total_amount += v['fine_amount']

        result.append(f'Total points: {total_points}\nTotal amount: {total_amount}')
        return '\n'.join(result)


    def get_top_drivers_by_points(self) -> str:
        violation = self.violation_repository.get_driver_points()
        result = []
        if not violation:
            print(f'No driver points')
        for v in violation:
            result.append(f"Driver name: {v['first_name']} {v['last_name']} has {v['total_points']} points")
        return '\n'.join(result)

    def get_speed_camera_statistic(self) -> dict[str, int]:
        violation = self.violation_repository.get_most_popular_speed_camera()
        if not violation:
            print(f'Speed camera has no violations')

        cameras: dict[str, int] = {}
        for v in violation:
            cameras[v['location']] = v['total_count']

        return cameras

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



