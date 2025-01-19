from bluetooth.socket_connection import SocketConnection
import threading


class Server(SocketConnection):
    is_server = True

    def connect(self):
        # Start server
        if self.is_server_connected:
            return
        self.is_server_connected = True
        self.socket.bind((self.address, self.port))
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
