import socket
from django.views import View
from django.shortcuts import render


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_msg(self, msg: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            if not msg:
                s.sendall("Failed".encode())
            else:
                s.sendall(msg.encode())
            
            data = s.recv(1024)

        print(f"Received {data!r}")


class IndexView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        context = {"title": "Cliente"}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        host = request.POST.get("host")
        port = request.POST.get("port")
        msg = request.POST.get("msg")

        if len(msg) == 0:
            msg = None 

        client = Client(host, int(port))
        client.send_msg(msg)
        
        context = {"title": "Cliente"}
        return render(request, self.template_name, context)
