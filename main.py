from src.database import MySQLConnectionManager
from src.execute_sql_file import SqlFileExecutor
from src.repository import (
    DriverRepository,
    SpeedCameraRepository,
    ViolationRepository,
    OffenseRepository
)
from src.service import ViolationService


def main() -> None:
    mysql_connection_manager = MySQLConnectionManager()

    # sql_executor = SqlFileExecutor(mysql_connection_manager)
    # sql_executor.execute_sql_file('sql/schema.sql')
    # sql_executor.execute_sql_file('sql/data.sql')

    driver_repository = DriverRepository(mysql_connection_manager)
    offense_repository = OffenseRepository(mysql_connection_manager)
    speed_camera_repository = SpeedCameraRepository(mysql_connection_manager)
    violation_repository = ViolationRepository(mysql_connection_manager)

    service = ViolationService(driver_repository, speed_camera_repository, offense_repository, violation_repository)
    service1 = service.get_offenses_by_driver('K123456')
    for driver_offense in service1:
        print(driver_offense)

    print('--------------------------------- [1] ---------------------------------')

    service2 = service.get_top_drivers_by_points()
    for driver_offense in service2:
        print(driver_offense)

    print('--------------------------------- [2] ---------------------------------')

    service3 = service.get_speed_camera_statistic()
    for driver_offense in service3:
        print(driver_offense)

    print('--------------------------------- [3] ---------------------------------')

    service4 = service.get_generate_report()
    for driver_offense in service4:
        print(driver_offense)










    # print(service.get_summary_statistic())


if __name__ == '__main__':
    main()