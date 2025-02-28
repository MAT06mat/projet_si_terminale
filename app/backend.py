from kivy.storage.jsonstore import JsonStore
from kivy.clock import mainthread
from imports import bluetooth_socket as bs
from threading import Thread
import os


class BluetoothClient(bs.Client):
    on_succes = None
    on_error = None

    def connect(self, on_succes, on_error):
        self.on_succes = mainthread(on_succes)
        self.on_error = mainthread(on_error)
        Thread(target=self._async_connect, daemon=True).start()

    def _async_connect(self):
        if callable(self.on_succes) and callable(self.on_error):
            try:
                super().connect()
                self.on_succes()
            except Exception as e:
                self.on_error(e)
            finally:
                self.on_succes = None
                self.on_error = None


bluetoothClient = BluetoothClient("B8:27:EB:80:0B:6D")


class Store(JsonStore):
    def put(self, key, value):
        return super().put(key, value=value)

    def get(self, key):
        return super().get(key)["value"]


os.makedirs(".cache", exist_ok=True)
settings = Store(".cache/settings.json")
cubeSaves = Store(".cache/cube_saves.json")
