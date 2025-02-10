from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import mainthread, Clock
from threading import Thread
from ui.popup import Error

from imports import bluetooth_socket

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
        self.client = bluetooth_socket.Client("")

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
        Clock.schedule_once(self.start_thread, 0.5)

    def start_thread(self, *args):
        Thread(target=self.bluetooth_connection_thread).start()

    def bluetooth_connection_thread(self):
        try:
            self.client.connect()
            self.bluetooth_connection_callback()
        except Exception as e:
            self.bluetooth_connection_callback(e)

    @mainthread
    def bluetooth_connection_callback(self, e=None):
        Clock.schedule_once(self.toogle_loading, 0.5)
        if e:
            Error(e).open()
