from comm.client import CommandClient

class Main:
    client = CommandClient(host="127.0.0.1", port=8080)
    client.connect()
    client.send_command("PING")
    client.close()

if __name__ == '__main__':
    Main()