from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import Clock
from ui.popup import Error

from imports import bluetooth_socket
from backend import bluetoothClient

Builder.load_file("screens/bluetooth_menu.kv")


class BluetoothMenu(MDBoxLayout):
    loading = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_loading = Animation(
            size=(dp(48), dp(48)), opacity=1, d=0.5, t="in_out_cubic"
        )
        self.stop_loading = Animation(
            size=(dp(20), 0), opacity=0, d=0.5, t="in_out_cubic"
        )
        self.bind(loading=self.on_loading)
        self.client = bluetoothClient

    def on_loading(self, *args):
        if self.loading:
            self.start_loading.start(self.ids.progress)
            self.stop_loading.cancel(self.ids.progress)
        else:
            self.stop_loading.start(self.ids.progress)
            self.start_loading.cancel(self.ids.progress)

    def toogle_loading(self, *args):
        self.loading = not self.loading

    def connect_bluetooth(self, *args):
        if self.loading:
            return
        self.loading = True
        Clock.schedule_once(self.start_connection, 0.5)

    def start_connection(self, *args):
        def on_succes():
            Clock.schedule_once(self.toogle_loading, 0.5)
            self.client.send(bluetooth_socket.Request.call("start_solver"))

        def on_error(e):
            Clock.schedule_once(self.toogle_loading, 0.5)
            Error(str(e))

        self.client.connect(on_succes, on_error)
