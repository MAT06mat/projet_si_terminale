from socket_connection import SocketConnection
import threading


class Client(SocketConnection):
    def connect(self):
        # Connect to server
        if self.client:
            return
        self.socket.connect((self.address, self.port))
        self.client = self.socket
        print("client-connected")
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Disconnect from server
        self.client.close()
