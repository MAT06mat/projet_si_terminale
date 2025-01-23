from bluetooth_socket.request import Request
import socket


class SocketConnection:
    public_vars = ["callback"]
    is_server = False
    uuid = "00001101-0000-1000-8000-00805F9B34FB"

    def __init__(self, address, port=4, bluetooth=True, request_lenght=512):
        self.address = address
        self.port = port

        # Set the request length for the Request class
        self.request_lenght = request_lenght
        Request.REQUEST_LENGHT = request_lenght

        # Initialize socket and connection variables
        if bluetooth and hasattr(socket, "AF_BLUETOOTH"):
            from bluetooth import BluetoothSocket, RFCOMM
            self.socket = BluetoothSocket(RFCOMM)
        elif not bluetooth:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.socket = None
            self.recv_stream = None
            self.send_stream = None

        self.client = None
        self.is_server_connected = False

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Accept client connection if server
                if not self.client and self.is_server:
                    self.client, addr = self.socket.accept()
                    print("Client socket accepted as", addr)
                # Receive data from client
                data = self.recv(self.request_lenght * 8)
                if data:
                    buffer += data
            except (ConnectionAbortedError, OSError) as e:
                if self.is_server_connected:
                    self.client = None
                    continue
                print("Loop stopped")
                return

            # Process received data
            while len(buffer) >= self.request_lenght:
                request = Request.decode(buffer[: self.request_lenght])
                buffer = buffer[self.request_lenght :]

                # Handle CALL requests
                if "CALL" in request:
                    if request["CALL"]["fname"] in self.public_vars:
                        func = self.__getattribute__(request["CALL"]["fname"])
                        func(*request["CALL"]["args"])

                # Handle GET requests
                if "GET" in request:
                    if request["GET"]["var"] in self.public_vars:
                        fid = request["GET"]["fid"]
                        value = self.__getattribute__(request["GET"]["var"])
                        response = Request.call("callback", fid, value)
                        self.send(response)

                # Handle SET requests
                if "SET" in request:
                    if request["SET"]["var"] in self.public_vars:
                        self.__setattr__(request["SET"]["var"], request["SET"]["value"])

    def callback(self, *args):
        # Handle callback
        Request.callback(*args)

    def recv(self, bufsize):
        return self.client.recv(bufsize)

    def send(self, request):
        # Send request to client or the server
        try:
            self.client.send(request)
        except ConnectionResetError:
            pass
