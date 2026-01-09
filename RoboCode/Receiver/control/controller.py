from hardware.driver import RobotDriver

class Controller:
    def __init__(self, driver:RobotDriver):
        self.driver = driver

    def move(self, v, omega):
        left, right, pend = self.driver.diffDriveKinematics.calculate_wheel_speeds(v, omega)
        self.driver.drive(left, right, pend)
        print(f"[CTRL] MOVE v={v}, omega={omega}")

    def stop(self):
        self.driver.stop_all()
        print("[CTRL] STOP")
