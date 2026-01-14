from comm.client import CommandClient
from comm.protocol import parse_command
import keyboard
import threading
import time

KEY_MAP = {
    'up': (1,0),
    'down': (-1,0),
    'left': (0,-1),
    'right': (0,1)
}


class Main:
    def __init__(self):
        try:
            self.client = CommandClient(host="10.12.82.132", port=8080)
            while self.client.connected==False:
                self.client.connect()
                self.client.send_command(parse_command("PING"))

                # Uruchamiamy listener w osobnym wątku
                listener_thread = threading.Thread(target=self.keyboard_listener)
                listener_thread.daemon = True
                listener_thread.start()

                # Główny loop
                while self.client.connected:
                    time.sleep(50)
                    self.client.send_command(parse_command("PING"))

        except Exception as e:
            self.client.close()
            print(e)

    def keyboard_listener(self):
        last = (0, 0)
        was_stopped = False

        while self.client.connected:
            dx, dy = 0, 0
            any_pressed = False

            # 1. Sprawdzenie spacji (PRIORYTET)
            if keyboard.is_pressed('space'):
                if not was_stopped:
                    print("STOP")
                    self.client.send_command(parse_command("STOP"))
                    was_stopped = True
                    last = (0, 0)  # Resetujemy kierunek po stopie
                time.sleep(0.05)
                continue  # Przeskakujemy resztę pętli, póki spacja jest trzymana

            # 2. Sprawdzenie kierunków
            for key in KEY_MAP:
                if keyboard.is_pressed(key):
                    any_pressed = True
                    vx, vy = KEY_MAP[key]
                    dx += vx
                    dy += vy

            current = (dx, dy)

            # 3. Wysyłanie komendy ruchu
            if current != last and any_pressed:
                cmd = f"MOVE {dx} {dy}"
                print(f"MOVE {dx} {dy}")
                self.client.send_command(parse_command(cmd))
                last = current
                was_stopped = False

            time.sleep(0.05)


if __name__ == '__main__':
    Main()
