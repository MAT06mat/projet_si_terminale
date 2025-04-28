from mods.bluetooth_socket.socket_connection import SocketConnection
import threading, socket


class Client(SocketConnection):
    on_deconnect = None

    def __init__(self, address, port=4, request_lenght=512):
        super().__init__(request_lenght)
        self.address = address
        self.port = port

        # Initialize socket and connection variables
        if hasattr(socket, "AF_BLUETOOTH"):
            self.socket = socket.socket(
                socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM
            )
        else:
            self.socket = None
            self.recv_stream = None
            self.send_stream = None

        self.connected = False

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Receive data from server
                data = self.recv(self.request_lenght * 8)
                if data:
                    buffer += data
            except (ConnectionAbortedError, OSError) as e:
                print("Loop stopped")
                self.connected = False
                self.on_deconnect()
                return
            self.process_data(buffer)

    def recv(self, bufsize):
        return self.socket.recv(bufsize)

    def send(self, request):
        # Send request to the server
        try:
            self.socket.send(request)
        except ConnectionResetError:
            pass

    def connect(self):
        # Connect to server
        self.socket.connect((self.address, self.port))
        print("client-connected")
        self.connected = True
        threading.Thread(target=self.loop, daemon=True).start()

    def deconnect(self):
        # Disconnect from server
        self.connected = False
        self.socket.close()
