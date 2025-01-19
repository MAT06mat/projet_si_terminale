from socket_connection import SocketConnection
from jnius import autoclass
import threading

BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
BluetoothDevice = autoclass("android.bluetooth.BluetoothDevice")
BluetoothSocket = autoclass("android.bluetooth.BluetoothSocket")
InputStreamReader = autoclass("java.io.InputStreamReader")
BufferedReader = autoclass("java.io.BufferedReader")
UUID = autoclass("java.util.UUID")


class AndroidClient(SocketConnection):
    is_android = True

    def android_get_socket_stream(self):
        if not self.is_android:
            return
        # Get the paired Bluetooth devices
        paired_devices = (
            BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        )
        self.socket = None
        for device in paired_devices:
            if device.getAddress() == self.address:
                # Create a socket to the device
                self.socket = device.createRfcommSocketToServiceRecord(
                    UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                )
                self.send_stream = self.socket.getOutputStream()
                reader = InputStreamReader(self.socket.getInputStream(), "UTF-8")
                self.recv_stream = BufferedReader(reader)
                break

    def connect(self):
        # Connect to server
        if not self.socket:
            self.android_get_socket_stream()
            self.socket.connect()
            print("client-connected")
            threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Disconnect from server
        if self.socket:
            self.socket.close()
            self.socket = None
            self.recv_stream = None
            self.send_stream = None

    def recv(self, bufsize):
        # Receive data from the server
        ready_to_read = self.recv_stream.ready()
        if not ready_to_read:
            return b""
        data = self.recv_stream.read(bufsize)
        return data.encode("utf-8")

    def send(self, request):
        # Send request to server
        self.send_stream.write(request)
        self.send_stream.flush()
