from kivy.logger import Logger
from imports import bluetooth_socket as bs


class BluetoothClient(bs.Client):
    _current_client: bs.Client | None = None

    def get_client():
        return BluetoothClient._current_client

    def __init__(self, address, port=4, request_lenght=512):
        super().__init__(address, port, request_lenght)
        if BluetoothClient._current_client:
            Logger.warning("BluetoothClient is created multiple times")
        BluetoothClient._current_client = self
