import socket, dotenv, os
from request import Request

dotenv.load_dotenv()


ADRESSE = os.getenv("ADRESSE")
PORT = os.getenv("PORT")


class Bluetooth:
    public_vars = ["callback", "a", "b", "c", "d"]

    def __init__(self):
        self.socket = socket.socket(
            socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
        )
        self.socket.setblocking(False)
        self.client = None
        self.connected = False

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

    def client_deconnect(self):
        self.send(Request.encode({"DECONNECT"}))
        self.client.close()

    def recv(self):
        if not self.client:
            return
        data = self.client.recv(4096)
        if not data:
            return
        json = Request.decode(data)

        if "CALL" in json:
            if json["CALL"]["fname"] in self.public_vars:
                func = self.__getattribute__(json["CALL"]["fname"])
                func(*json["CALL"]["args"])

        if "GET" in json:
            if json["GET"]["var"] in self.public_vars:
                fid = json["GET"]["fid"]
                value = self.__getattribute__(json["GET"]["var"])
                request = Request.call("callback", fid, value)
                self.send(request)

        if "SET" in json:
            if json["SET"]["var"] in self.public_vars:
                self.__setattr__(json["SET"]["var"], json["SET"]["value"])

        if "DECONNECT" in json:
            self.client.close()
            self.client = None

    def callback(self, *args):
        Request.callback(*args)

    def send(self, request):
        self.client.send(request)
