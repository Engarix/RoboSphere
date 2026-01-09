import socket
from comm.protocol import parse_command, ProtocolError
from comm.client_state import ClientState


class CommandServer:
    def __init__(self, host: str, port: int, timeout: float, controller):
        self.host = host
        self.port = port
        self.controller = controller
        self.client_state = ClientState(timeout)
        print("Server initialized")

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(1)

            print(f"[COMM] Listening on {self.host}:{self.port}")

            while True:
                conn, addr = sock.accept()
                print(f"[COMM] Client connected: {addr}")
                self.handle_client(conn)

    def handle_client(self, conn: socket.socket):
        with conn:
            conn.settimeout(self.client_state.timeout)

            while True:
                try:
                    data = conn.recv(1024)
                    if not data:
                        print("[COMM] Client disconnected")
                        self.controller.stop()
                        break

                    raw = data.decode("utf-8")
                    for line in raw.splitlines():
                        self._handle_line(line, conn)

                except socket.timeout:
                    if self.client_state.expired():
                        self.controller.stop()
                        self.client_state.reset()

                except Exception as e:
                    print(f"[COMM] Error: {e}")
                    self.controller.stop()
                    break

    def _handle_line(self, line: str, conn: socket.socket):
        try:
            cmd = parse_command(line)
            self.client_state.update()

            if cmd.name == "MOVE":
                v, omega = cmd.args
                self.controller.move(v, omega)

            elif cmd.name == "STOP":
                self.controller.stop()

            elif cmd.name == "PING":
                conn.sendall(b"PONG\n")

            elif cmd.name == "INFO":
                print(f"[INFO] {' '.join(cmd.args)}")

        except ProtocolError as e:
            conn.sendall(f"ERR {e}\n".encode("utf-8"))
