from config import robotSettings

class DiffDriveKinematics:
    def __init__(self):
        self.curr_left = 0.0
        self.curr_right = 0.0
        self.curr_pend = 0.0

    def reset(self):
        self.curr_left = 0.0
        self.curr_right = 0.0
        self.curr_pend = 0.0

    def _approach(self, current, target):
        if current < target:
            return min(target, current + robotSettings.ACCELERATION_PERCENTAGE)
        elif current > target:
            return max(target, current - robotSettings.ACCELERATION_PERCENTAGE)
        return target

    def calculate_wheel_speeds(self, v: float, omega: float):

        pendulum_speed = abs(v) * omega

        if v == 0:
            left_speed = v + omega
            right_speed = v - omega
        elif v == 1:
            left_speed = v * ((v-omega)//2 + (v-omega)%2)
            right_speed = v * ((v+omega)//2 + (v+omega)%2)
        elif v == -1:
            left_speed = v * (abs(v+omega)//2 + (v+omega)%2)
            right_speed = v * (abs(v-omega)//2 + (v-omega)%2)
        else:
            left_speed = 0
            right_speed = 0

        self.curr_left = self._approach(self.curr_left, left_speed)
        self.curr_right = self._approach(self.curr_right, right_speed)
        self.curr_pend = self._approach(self.curr_pend, pendulum_speed)

        return self.curr_left, self.curr_right, self.curr_pend

    # 1 0 = l 1 r 1
    # 1 1 = l 0 r 1
    # 1 -1 = l 1 r 0

    # 0 0 = l 0 r 0
    # 0 1 = l 1 r -1
    # 0 -1 = l -1 r 1

    # -1 0 = l -1 r -1
    # -1 1 = l 0 r -1
    # -1 -1 = l -1 r 0
