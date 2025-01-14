import socket
from request import Request

ADRESSE = ""
PORT = 4


class Bluetooth:
    public_vars = ["callback", "a", "b", "c", "d"]

    def __init__(self):
        self.socket = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
        )
        self.socket.setblocking(False)
        self.client = None

        self.a = 1
        self.b = 5
        self.c = "test"
        self.d = "^ç^"

    def client_connect(self):
        if self.client:
            return
        self.socket.connect((ADRESSE, PORT))
        self.client = self.socket
        print("client-connected")

    def server_connect(self):
        if self.client:
            return
        self.socket.bind((ADRESSE, PORT))
        self.socket.listen(1)
        print("server-online")
        self.client, addr = self.socket.accept()
        print("server-connected")

    def recv(self):
        if not self.client:
            return
        data = self.client.recv(1024)
        json = Request.decode(data)

        if "call" in json:
            if json["call"]["fname"] in self.public_vars:
                func = self.__getattribute__(json["call"]["fname"])
                func(*json["call"]["args"])

        if "get" in json:
            if json["get"]["var"] in self.public_vars:
                fid = json["get"]["fid"]
                value = self.__getattribute__(json["get"]["var"])
                request = Request.call("callback", fid, value)
                self.send(request)

        if "set" in json:
            if json["set"]["var"] in self.public_vars:
                self.__setattr__(json["set"]["var"], json["set"]["value"])

    def callback(self, *args):
        Request.callback(*args)

    def send(self, request):
        self.client.send(request)
