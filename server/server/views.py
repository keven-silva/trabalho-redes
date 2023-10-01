import socket
import os
import pickle
import threading
import datetime


from django.views import View
from django.shortcuts import render
from googletrans import Translator


class Server:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def close(self):
        self.server_socket.close()

    def send_msg_to_client(self, conn):
        translator = Translator(
            service_urls=[
                "translate.google.com",
            ]
        )

        data = conn.recv(4096)
        if not data:
            return None

        data_pkl = pickle.loads(data)

        translated_language = translator.translate(data_pkl["msg"], dest="en")
        translated_language = translated_language.text
        print(f"Message: {translated_language}")

        files = os.listdir("server/")
        hour = datetime.datetime.now().strftime("%H:%M:%S")
        # read_file = open(f"server/{data_pkl['file_name']}", "r")

        data_dict = {
            "files": files,
            "message": translated_language,
            "hour": hour,
            # "data_file": read_file.read(),
        }
        pkl = pickle.dumps(data_dict)

        conn.send(pkl)


# Global dictionary to store server instances
global servers
servers = {}


class IndexView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        host = "127.0.0.1"
        self.port = int(request.POST.get("port"))

        # Verifica se ainda pode ligar portas (máximo 10)
        if len(servers) >= 10:
            context = {
                "ports": servers,
                "port_already_connected": 0,
                "port_created": 0,
                "ports_maximum": self.port,
                "port_closed": 0,
            }
            return render(request, self.template_name, context)

        # Verifica se a porta já está ligada
        if str(self.port) in servers:
            context = {
                "ports": servers,
                "port_already_connected": self.port,
                "port_created": 0,
                "ports_maximum": 0,
                "port_closed": 0,
            }
            return render(request, self.template_name, context)

        # Create and start the server
        server = Server(host, self.port)
        servers[f"{self.port}"] = server
        threading.Thread(target=self.handle_client, args=(server,)).start()

        context = {
            "ports": servers,
            "port_already_connected": 0,
            "port_created": self.port,
            "ports_maximum": 0,
            "port_closed": 0,
        }
        return render(request, self.template_name, context)

    def handle_client(self, server):
        while True:
            conn, addr = server.server_socket.accept()
            threading.Thread(target=self.handle_client_connection, args=(conn,)).start()

    def handle_client_connection(self, conn):
        try:
            server_port = conn.getsockname()[1]
            server = servers.get(str(server_port))
            if server:
                server.send_msg_to_client(conn)
            else:
                print(f"No server found for port {server_port}")
        except Exception as e:
            return f"Error handling client connection: {e}"


class DisconnectView(View):
    def get(self, request, *args, **kwargs):
        context = {"ports": servers}
        return render(request, "base.html", context)

    def post(self, request, *args, **kwargs):
        conn_port = request.POST.get("port")
        aux = 0

        for port, server in servers.items():
            if port == conn_port:
                server.close()
                aux = port
        if aux:
            servers.pop(aux)

        context = {
            "ports": servers,
            "port_already_connected": 0,
            "port_created": 0,
            "ports_maximum": 0,
            "port_closed": aux,
        }

        return render(request, "base.html", context)
