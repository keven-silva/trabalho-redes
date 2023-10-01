import socket
import pickle
from django.views import View
from django.shortcuts import render


class Client:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def send_msg(self, data_to_serve: str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            if not data_to_serve:
                s.sendall("Vázio".encode())
            else:
                data_to_serve = pickle.dumps(data_to_serve)
                s.sendall(data_to_serve)

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
        file_name = request.POST.get("file_name")
        msg = request.POST.get("msg")

        if len(msg) == 0:
            msg = None

        client = Client(host, int(port))
        data_to_serve = {"file_name": file_name, "msg": msg}

        data = client.send_msg(data_to_serve)
        # create_file(data['data_file'])

        context = {
            "title": "Cliente",
            "msg": data["message"],
            "hour": data["hour"],
            "files": data["files"],
        }
        return render(request, self.template_name, context)


def create_file(data: str):
    with open("client/client/file.txt", "w") as f:
        f.write(data)
