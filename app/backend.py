from kivy.logger import Logger
from kivy.clock import mainthread
from imports import bluetooth_socket as bs
from threading import Thread


class BluetoothClient(bs.Client):
    _current_client: bs.Client | None = None
    on_succes = None
    on_error = None

    def get_client():
        return BluetoothClient._current_client

    def __init__(self, address, port=4, request_lenght=512):
        super().__init__(address, port, request_lenght)
        if BluetoothClient._current_client:
            Logger.warning("BluetoothClient is created multiple times")
        BluetoothClient._current_client = self

    def connect(self, on_succes, on_error):
        self.on_succes = mainthread(on_succes)
        self.on_error = mainthread(on_error)
        Thread(target=self.async_connect).start()

    def async_connect(self):
        if self.on_succes and self.on_error:
            try:
                super().connect()
                self.on_succes()
            except Exception as e:
                self.on_error(e)
            finally:
                self.on_succes = None
                self.on_error = None
