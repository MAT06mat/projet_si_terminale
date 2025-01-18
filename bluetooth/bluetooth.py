import socket, dotenv, os, threading
from bluetooth.request import Request

dotenv.load_dotenv()

# Load address and port from environment variables
ADRESSE = os.getenv("ADRESSE")
PORT = os.getenv("PORT")
REQUEST_LENGHT = 512

# Set the request length for the Request class
Request.REQUEST_LENGHT = REQUEST_LENGHT


class SocketConnection:
    public_vars = ["callback", "a", "b", "c", "d"]
    is_server = False

    def __init__(self):
        # Initialize socket and connection variables
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM  # , socket.BTPROTO_RFCOMM
        )
        self.client = None
        self.connected = False
        self.is_server_connected = False

        # Example variables
        self.a = 1
        self.b = 5
        self.c = "test"
        self.d = "^ç^"

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Accept client connection if server
                if not self.client and self.is_server:
                    self.client, addr = self.socket.accept()
                # Receive data from client
                buffer += self.client.recv(REQUEST_LENGHT * 8)
            except (ConnectionAbortedError, OSError) as e:
                if self.is_server_connected:
                    self.client = None
                    continue
                print("Loop stopped")
                return

            # Process received data
            while len(buffer) >= REQUEST_LENGHT:
                json = Request.decode(buffer[:REQUEST_LENGHT])
                buffer = buffer[REQUEST_LENGHT:]

                # Handle CALL requests
                if "CALL" in json:
                    if json["CALL"]["fname"] in self.public_vars:
                        func = self.__getattribute__(json["CALL"]["fname"])
                        func(*json["CALL"]["args"])

                # Handle GET requests
                if "GET" in json:
                    if json["GET"]["var"] in self.public_vars:
                        fid = json["GET"]["fid"]
                        value = self.__getattribute__(json["GET"]["var"])
                        request = Request.call("callback", fid, value)
                        self.send(request)

                # Handle SET requests
                if "SET" in json:
                    if json["SET"]["var"] in self.public_vars:
                        self.__setattr__(json["SET"]["var"], json["SET"]["value"])

    def callback(self, *args):
        # Handle callback
        Request.callback(*args)

    def send(self, request):
        # Send request to client
        try:
            self.client.send(request)
        except ConnectionResetError:
            pass


class Client(SocketConnection):
    is_server = False

    def connect(self):
        # Connect to server
        if self.client:
            return
        self.socket.connect((ADRESSE, int(PORT)))
        self.client = self.socket
        print("client-connected")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Disconnect from server
        self.client.close()


class Server(SocketConnection):
    is_server = True

    def connect(self):
        # Start server
        if self.is_server_connected:
            return
        self.is_server_connected = True
        self.socket.bind((ADRESSE, int(PORT)))
        self.socket.listen(1)
        print("server-online")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Stop server
        if self.is_server_connected:
            self.is_server_connected = False
            if self.client:
                self.client.close()
            self.socket.close()
