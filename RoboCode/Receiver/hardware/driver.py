from gpiozero import PWMOutputDevice, DigitalOutputDevice
from config import robotSettings
from kinematics import DiffDriveKinematics

class Motor:
    """Obsługa pojedynczego silnika (PWM + 2 piny kierunkowe)"""
    def __init__(self, pwm_pin, fwd_pin, back_pin):
        self.pwm = PWMOutputDevice(pwm_pin)
        self.fwd = DigitalOutputDevice(fwd_pin)
        self.back = DigitalOutputDevice(back_pin)

    def set_speed(self, speed):
        """Ustawia prędkość od -1.0 do 1.0"""
        if speed > 0:
            self.fwd.on()
            self.back.off()
            self.pwm.value = speed
        elif speed < 0:
            self.fwd.off()
            self.back.on()
            self.pwm.value = abs(speed)
        else:
            self.stop()

    def stop(self):
        self.fwd.off()
        self.back.off()
        self.pwm.value = 0

class RobotDriver:
    def __init__(self):
        # Inicjalizacja silników zgodnie z Twoją konfiguracją pinów
        self.left_motor = Motor(robotSettings.PWM_LEFT, robotSettings.MOTOR_LEFT_F, robotSettings.MOTOR_LEFT_B)
        self.right_motor = Motor(robotSettings.PWM_RIGHT, robotSettings.MOTOR_RIGHT_F, robotSettings.MOTOR_RIGHT_B)
        self.pendulum = Motor(robotSettings.PWM_PENDULUM, robotSettings.MOTOR_PENDULUM_F, robotSettings.MOTOR_PENDULUM_B)
        self.diffDriveKinematics = DiffDriveKinematics()
        print("RobotDriver initialized")

    def drive(self, left_speed, right_speed, pendulum_speed):
        """Sterowanie napędem różnicowym"""
        self.left_motor.set_speed(left_speed)
        self.right_motor.set_speed(right_speed)
        self.pendulum.set_speed(pendulum_speed)

    def stop_all(self):
        self.left_motor.stop()
        self.right_motor.stop()
        self.pendulum.stop()
        self.diffDriveKinematics.reset()