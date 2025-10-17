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
    # print(service.get_offenses_by_driver('K123456'))
    # print(service.get_top_drivers_by_points())
    # print(service.get_speed_camera_statistic())
    # print(service.get_summary_statistic())


if __name__ == '__main__':
    main()