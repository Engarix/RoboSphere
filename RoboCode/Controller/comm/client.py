import socket
from comm.protocol import format_command, ProtocolError

class CommandClient:
    def __init__(self, host: str, port: int, timeout: float = 1.0):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        print(f"[COMM] Connected to {self.host}:{self.port}")

    def send_command(self, name: str, *args):
        if not self.sock:
            raise ConnectionError("Client is not connected")

        try:
            cmd_str = format_command(name, *args) + "\n"  # np. "MOVE 1 0\n"
            self.sock.sendall(cmd_str.encode("utf-8"))

            # opcjonalnie odczyt odpowiedzi (np. PONG)
            try:
                resp = self.sock.recv(1024)
                if resp:
                    print(f"[COMM] Response: {resp.decode('utf-8').strip()}")
            except socket.timeout:
                pass

        except ProtocolError as e:
            print(f"[COMM] Protocol error: {e}")

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None
            print("[COMM] Disconnected")
