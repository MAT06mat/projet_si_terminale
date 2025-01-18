import socket, dotenv, os, threading
from bluetooth.request import Request

dotenv.load_dotenv()


ADRESSE = os.getenv("ADRESSE")
PORT = os.getenv("PORT")
REQUEST_LENGHT = 512


Request.REQUEST_LENGHT = REQUEST_LENGHT


class Bluetooth:
    public_vars = ["callback", "a", "b", "c", "d"]
    is_server = False

    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM  # , socket.BTPROTO_RFCOMM
        )
        self.client = None
        self.connected = False
        self.is_server_connected = False

        self.a = 1
        self.b = 5
        self.c = "test"
        self.d = "^ç^"

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                if not self.client and self.is_server:
                    self.client, addr = self.socket.accept()
                buffer += self.client.recv(REQUEST_LENGHT * 8)
            except (ConnectionAbortedError, OSError) as e:
                if self.is_server_connected:
                    self.client = None
                    continue
                print("Loop stopped")
                return

            while len(buffer) >= REQUEST_LENGHT:
                json = Request.decode(buffer[:REQUEST_LENGHT])
                buffer = buffer[REQUEST_LENGHT:]

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

    def callback(self, *args):
        Request.callback(*args)

    def send(self, request):
        try:
            self.client.send(request)
        except ConnectionResetError:
            pass


class Client(Bluetooth):
    is_server = False

    def connect(self):
        if self.client:
            return
        self.socket.connect((ADRESSE, int(PORT)))
        self.client = self.socket
        print("client-connected")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        self.client.close()


class Server(Bluetooth):
    is_server = True

    def connect(self):
        if self.is_server_connected:
            return
        self.is_server_connected = True
        self.socket.bind((ADRESSE, int(PORT)))
        self.socket.listen(1)
        print("server-online")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        if self.is_server_connected:
            self.is_server_connected = False
            if self.client:
                self.client.close()
            self.socket.close()
