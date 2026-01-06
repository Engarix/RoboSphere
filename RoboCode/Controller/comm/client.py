import socket
from comm.protocol import format_command, ProtocolError, Command


class CommandClient:
    def __init__(self, host: str, port: int, timeout: float = 0.5):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.sock = None
        self.connected = False

    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.timeout)
        self.sock.connect((self.host, self.port))
        self.connected = True
        print(f"[COMM] Connected to {self.host}:{self.port}")

    def send_command(self, cmd:Command):
        if not self.sock:
            raise ConnectionError("Client is not connected")

        try:
            cmd_str = format_command(cmd)
            self.sock.sendall(cmd_str)

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
            self.connected = False
            print("[COMM] Disconnected")
