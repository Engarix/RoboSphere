from comm.server import CommandServer
from control.controller import Controller
from config import network
from hardware.driver import RobotDriver

class Main:
    def __init__(self):
        driver = RobotDriver()
        controller = Controller(driver)
        server = CommandServer(host=network.HOST, port=network.PORT, timeout=network.SOCKET_TIMEOUT, controller=controller)
        server.start()

if __name__ == '__main__':
    Main()