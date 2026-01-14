import threading
import time
from hardware.driver import RobotDriver

class Controller:
    def __init__(self, driver: RobotDriver):
        self.driver = driver
        self.target_v = 0.0
        self.target_omega = 0.0
        self._stop_event = threading.Event()
        # Uruchamiamy wątek, który będzie co X ms aktualizował prędkość silników
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()

    def _update_loop(self):
        """Pętla działająca w tle, która płynnie dąży do prędkości docelowej"""
        while not self._stop_event.is_set():
            # Obliczamy nową prędkość (wykonuje jeden krok _approach)
            left, right, pend = self.driver.diffDriveKinematics.calculate_wheel_speeds(
                self.target_v, self.target_omega
            )
            # Fizycznie ustawiamy prędkość na sterowniku
            self.driver.drive(left, right, pend)

            # Częstotliwość aktualizacji (np. 20Hz = co 0.05s)
            time.sleep(0.05)

    def move(self, v, omega):
        """Tylko ustawia cel, pętla w tle zajmie się resztą"""
        self.target_v = v
        self.target_omega = omega
        print(f"[CTRL] TARGET SET v={v}, omega={omega}")

    def stop(self):
        self.target_v = 0
        self.target_omega = 0
        self.driver.stop_all()
        print("[CTRL] STOP")
