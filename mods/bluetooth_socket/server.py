from mods.bluetooth_socket.socket_connection import SocketConnection
from bluetooth import *
import threading


class Server(SocketConnection):
    def __init__(self, request_lenght=512):
        super().__init__(request_lenght)
        # Initialize socket and connection variables
        self.socket = BluetoothSocket(RFCOMM)

        self.client = None
        self.is_server_connected = False

    def loop(self):
        print("Loop started")
        buffer = b""
        while True:
            try:
                # Accept client connection
                if not self.client:
                    self.client, addr = self.socket.accept()
                    print("Client socket accepted as", addr)
                # Receive data from client
                data = self.recv(self.request_lenght * 8)
                if data:
                    buffer += data
            except (ConnectionAbortedError, OSError) as e:
                if self.is_server_connected:
                    print("Client disconnected")
                    self.client = None
                    continue
                print("Loop stopped")
                return
            self.process_data(buffer)

    def recv(self, bufsize):
        return self.client.recv(bufsize)

    def send(self, request):
        # Send request to client
        try:
            self.client.send(request)
        except ConnectionResetError:
            pass

    def connect(self):
        # Start server
        if self.is_server_connected:
            return
        self.is_server_connected = True
        self.socket.bind(("", PORT_ANY))
        self.socket.listen(1)
        self.port = self.socket.getsockname()[1]
        advertise_service(
            self.socket,
            "SampleServer",
            service_id=self.uuid,
            service_classes=[self.uuid, SERIAL_PORT_CLASS],
            profiles=[SERIAL_PORT_PROFILE],
        )
        print("server-online")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Stop server
        if self.is_server_connected:
            self.is_server_connected = False
            if self.client:
                self.client.close()
            self.socket.close()
