import socket


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def configure(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(b"Hello, world")
            data = s.recv(1024)

        print(f"Received {data!r}")


client = Client('localhost', 5000)
client.configure()
