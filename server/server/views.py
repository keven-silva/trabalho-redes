import socket
from django.views import View
from django.shortcuts import render
from concurrent import futures


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
                    if data == b"Failed":
                        conn.sendall(b"Failed")
                        return "","Failed"
                    else:
                        conn.sendall(data)
                    
                
                    return data, "Sucess"


class IndexView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        host = request.POST.get("host")
        port = request.POST.get("port")

        server = Server(host, int(port))
        future = futures.ThreadPoolExecutor().submit(server.configure)
        result, status = future.result()
        
        if result:
            result = result.decode()
        
        context = {"title": "Servidor", "connected": True, "message": result, "status": status}
        return render(request, self.template_name, context)