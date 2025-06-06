from kivy.storage.jsonstore import JsonStore
from kivy.clock import mainthread
from kivy.app import App
from imports import bluetooth_socket as bs
from threading import Thread
import os, sys


def get_saves_images_path(cube_string):
    filename = f"{cube_string}.png"
    if sys.platform == "win32":
        return os.path.join(".cache", "saves", filename)
    os.makedirs(App.get_running_app().user_data_dir, "saves", exist_ok=True)
    return os.path.join(App.get_running_app().user_data_dir, "saves", filename)


class BluetoothClient(bs.Client):
    _on_succes = None
    _on_error = None

    def connect(self, on_succes, on_error):
        self._on_succes = mainthread(on_succes)
        self._on_error = mainthread(on_error)
        Thread(target=self._async_connect, daemon=True).start()

    def _async_connect(self):
        if callable(self._on_succes) and callable(self._on_error):
            try:
                super().connect()
                self._on_succes()
            except Exception as e:
                self._on_error(e)
            finally:
                self._on_succes = None
                self._on_error = None


bluetoothClient = BluetoothClient("B8:27:EB:80:0B:6D")


class Store(JsonStore):
    def put(self, key, value):
        return super().put(key, value=value)

    def get(self, key):
        return super().get(key)["value"]


os.makedirs(".cache/saves", exist_ok=True)
settings = Store(".cache/settings.json")
cubeSaves = Store(".cache/cube_saves.json")
