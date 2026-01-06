from comm.server import CommandServer
from control.controller import Controller

class Main:
    controller = Controller()
    server = CommandServer(host="0.0.0.0", port=8080, timeout=0.5, controller=controller)
    server.start()


if __name__ == '__main__':
    Main()