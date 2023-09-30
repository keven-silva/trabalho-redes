import socket
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

            data = s.recv(1024)

        return f"{data.decode('utf-8')}"


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
        translated_msg = client.send_msg(msg)
        hour = datetime.datetime.now()

        context = {"title": "Cliente", "msg": translated_msg, "hour": hour}
        return render(request, self.template_name, context)
