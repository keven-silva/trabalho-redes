import socket


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def configure(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            conn, addr = s.accept()

            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    conn.sendall(data)


server = Server("127.0.0.1", 5000)
server.configure()
