import socket
from bluetooth.request import Request


class SocketConnection:
    public_vars = ["callback"]
    is_server = False

    def __init__(self, address, port, request_lenght=512):
        self.address = address
        self.port = port

        # Set the request length for the Request class
        self.request_lenght = request_lenght
        Request.REQUEST_LENGHT = request_lenght

        # Initialize socket and connection variables
        self.socket = socket.socket(
            socket.AF_INET, socket.SOCK_STREAM  # , socket.BTPROTO_RFCOMM
        )
        self.client = None
        self.connected = False
        self.is_server_connected = False

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Accept client connection if server
                if not self.client and self.is_server:
                    self.client, addr = self.socket.accept()
                # Receive data from client
                buffer += self.client.recv(self.request_lenght * 8)
            except (ConnectionAbortedError, OSError) as e:
                if self.is_server_connected:
                    self.client = None
                    continue
                print("Loop stopped")
                return

            # Process received data
            while len(buffer) >= self.request_lenght:
                json = Request.decode(buffer[: self.request_lenght])
                buffer = buffer[self.request_lenght :]

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
