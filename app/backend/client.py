from backend.bluetooth_socket import SocketConnection
import threading


class Client(SocketConnection):
    def connect(self):
        # Connect to server
        self.socket.connect((self.address, self.port))
        print("client-connected")
        self.connected = True
        threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Disconnect from server
        self.connected = False
        self.socket.close()
