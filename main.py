from src.entity import Driver, SpeedCamera, Offense, Violation
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
    # service.add_driver(Driver(first_name='x', last_name='y', registration_number='xxx'))
    print(service.get_offenses_by_driver('K123456'))
    # print(service.get_top_drivers_by_points())

    # print(service.get_camera_violations())
    # print(service.get_summary_statistic())

    # speed_cameras = speed_camera_repository.find_all()
    # for speed_camera in speed_cameras:
    #     print(speed_camera)

    # print(speed_camera_repository.find_by_id(1))
    # print(speed_camera_repository.delete(5))

    # speed_camera_repository.update(2, SpeedCamera(location='aaa', allowed_speed=-1))
    # speed_camera_repository.insert_many([
    #     SpeedCamera(location='XXX', allowed_speed=220),
    #     SpeedCamera(location='YYY', allowed_speed=230)
    # ])

    # speed_camera_repository.insert(SpeedCamera(location='ZZZ', allowed_speed=230))

    #
    # driver_repository = DriverRepository(mysql_connection_manager)
    # print(driver_repository.find_all())
    #
    # offense_repository = OffenseRepository(mysql_connection_manager)
    # print(offense_repository.find_all())
    #
    # violation_repository = ViolationRepository(mysql_connection_manager)
    # print(violation_repository.find_all())


if __name__ == '__main__':
    main()