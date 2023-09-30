import socket
import pickle
from django.views import View
from django.shortcuts import render
import datetime


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_msg(self, msg: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            if not msg:
                s.sendall("Vázio".encode())
            else:
                s.sendall(msg.encode())

            data = s.recv(4096)
            data_dict = pickle.loads(data)

        return data_dict


class IndexView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        context = {"title": "Cliente"}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        host = "127.0.0.1"
        port = request.POST.get("port")
        msg = request.POST.get("msg")

        if len(msg) == 0:
            msg = None

        client = Client(host, int(port))
        data = client.send_msg(msg)
        create_file(data)

        context = {
            "title": "Cliente",
            "msg": data["message"],
            "hour": data["hour"],
            "files": data["files"],
        }
        return render(request, self.template_name, context)


def create_file(data: dict):
    with open("client/client/file.txt", "w") as f:
        f.write(f"Message: {data['message']}\n")
        f.write(f"Hour: {data['hour']}\n")
        f.write(f"Files: {data['files']}\n")
