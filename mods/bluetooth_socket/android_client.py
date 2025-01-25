from android.permissions import request_permissions, check_permission, Permission
from mods.bluetooth_socket.client import Client
from jnius import autoclass

import threading


BluetoothAdapter = autoclass("android.bluetooth.BluetoothAdapter")
InputStreamReader = autoclass("java.io.InputStreamReader")
BufferedReader = autoclass("java.io.BufferedReader")
UUID = autoclass("java.util.UUID")


class AndroidClient(Client):
    def android_get_socket_stream(self):
        # Get the paired Bluetooth devices
        paired_devices = (
            BluetoothAdapter.getDefaultAdapter().getBondedDevices().toArray()
        )
        self.socket = None
        for device in paired_devices:
            if device.getAddress().upper() == self.address.upper():
                # Create a socket to the device
                self.socket = device.createRfcommSocketToServiceRecord(
                    UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
                )
                self.send_stream = self.socket.getOutputStream()
                self.recv_stream = self.socket.getInputStream()
                break

    def connect(self):
        # Connect to server
        if not self.socket:
            if not check_permission(Permission.BLUETOOTH_CONNECT):
                request_permissions([Permission.BLUETOOTH_CONNECT])
                return
            self.android_get_socket_stream()
            if not self.socket:
                return
            self.socket.connect()
            self.connected = True
            threading.Thread(target=self.loop).start()

    def deconnect(self):
        # Disconnect from server
        if self.socket:
            self.socket.close()
            self.connected = False
            self.socket = None
            self.recv_stream = None
            self.send_stream = None

    def recv(self, _):
        # Receive data from the server
        if self.recv_stream:
            ready = self.recv_stream.available()
            if ready <= 0:
                return b""
            buffer = bytearray(ready)
            self.recv_stream.read(buffer)
            return bytes(buffer)

    def send(self, request):
        # Send request to server
        if self.send_stream:
            self.send_stream.write(request)
            self.send_stream.flush()
