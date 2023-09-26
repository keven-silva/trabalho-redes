import socket
from django.views import View
from django.shortcuts import render
from concurrent import futures
from googletrans import Translator


class Server:
    conn = ''
    addr = ''

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def init(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen()
        self.conn, self.addr = s.accept()

        self.send_msg_to_client()

    def clonse_connection(self):
        self.conn.close()

    def send_msg_to_client(self):
        translator = Translator(
            service_urls=[
                "translate.google.com",
            ]
        )

        data = self.conn.recv(1024)
        if not data:
            return None

        menssage = data.decode("utf-8")

        translated_language = translator.translate(menssage, dest="en")
        translated_language = translated_language.text
        print(f"Mensage: {translated_language}")
        self.conn.send(translated_language.encode())


class IndexView(View):
    template_name = "base.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        with futures.ThreadPoolExecutor() as executor:
            host = request.POST.get("host")
            port = request.POST.get("port")
            futures_list = []

            server = Server(host, int(port))
            futures_list.append(executor.submit(server.init))

            for future in futures.as_completed(futures_list):
                result = future.result()
                print(f'Message: {result}')
                server.clonse_connection()
                return render(request, self.template_name, {})
