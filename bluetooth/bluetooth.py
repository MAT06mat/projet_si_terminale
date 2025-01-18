import socket, dotenv, os, threading
from bluetooth.request import Request

dotenv.load_dotenv()


ADRESSE = os.getenv("ADRESSE")
PORT = os.getenv("PORT")


class Bluetooth:
    public_vars = ["callback", "a", "b", "c", "d"]

    def __init__(self):
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM  # , socket.BTPROTO_RFCOMM
        )
        self.client = None
        self.connected = False
        self.is_server = False
        self.is_server_connected = False

        self.a = 1
        self.b = 5
        self.c = "test"
        self.d = "^ç^"

    def client_connect(self):
        if self.client:
            return
        self.socket.connect((ADRESSE, int(PORT)))
        self.client = self.socket
        print("client-connected")
        threading.Thread(target=self.loop).start()

    def server_connect(self):
        if self.is_server_connected:
            return
        self.is_server = True
        self.is_server_connected = True
        self.socket.bind((ADRESSE, int(PORT)))
        self.socket.listen(1)
        print("server-online")
        threading.Thread(target=self.loop).start()

    def client_deconnect(self):
        self.send(Request.encode({"DECONNECT": 1}))
        self.client.close()

    def server_deconnect(self):
        if self.is_server_connected:
            self.is_server_connected = False
            if self.client:
                self.client.close()
            self.socket.close()

    def loop(self):
        while self.is_server_connected or self.client:
            try:
                if not self.client and self.is_server:
                    self.client, addr = self.socket.accept()
                data = self.client.recv(4096)
            except (ConnectionAbortedError, KeyboardInterrupt, OSError) as e:
                self.server_deconnect()
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
        try:
            self.client.send(request)
        except ConnectionResetError:
            pass
