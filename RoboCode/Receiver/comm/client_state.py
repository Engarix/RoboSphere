import time

class ClientState:
    def __init__(self, timeout: float):
        self.timeout = timeout
        self.last_seen = time.monotonic()
        self.active = False

    def update(self):
        self.last_seen = time.monotonic()
        self.active = True

    def expired(self) -> bool:
        return (time.monotonic() - self.last_seen) > self.timeout

    def reset(self):
        self.active = False
