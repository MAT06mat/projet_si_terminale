from bluetooth_socket.socket_connection import SocketConnection
from bluetooth import *
import threading


class Server(SocketConnection):
    is_server = True

    def connect(self):
        # Start server
        if self.is_server_connected:
            return
        self.is_server_connected = True
        self.socket.bind(("", PORT_ANY))
        self.socket.listen(1)
        self.port = self.socket.getsockname()[1]
        advertise_service( self.socket, "SampleServer", service_id = self.uuid, service_classes = [ self.uuid, SERIAL_PORT_CLASS ], profiles = [ SERIAL_PORT_PROFILE ])
        print("server-online")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Stop server
        if self.is_server_connected:
            self.is_server_connected = False
            if self.client:
                self.client.close()
            self.socket.close()
