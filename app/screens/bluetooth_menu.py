from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import Clock
from ui.popup import Error, Info

from imports import bluetooth_socket
from backend import bluetoothClient

Builder.load_file("screens/bluetooth_menu.kv")


class BluetoothMenu(MDBoxLayout):
    loading = BooleanProperty(False)
    connected = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.start_loading = Animation(
            size=(dp(48), dp(48)), opacity=1, d=0.5, t="in_out_cubic"
        )
        self.stop_loading = Animation(
            size=(dp(20), 0), opacity=0, d=0.5, t="in_out_cubic"
        )
        self.anim_opacity_in = Animation(opacity=1, d=0.5, t="in_out_cubic")
        self.anim_opacity_out = Animation(opacity=0, d=0.5, t="in_out_cubic")
        self.bind(loading=self.on_loading)
        self.bind(connected=self.on_connected)
        self.client = bluetoothClient

    def opacity_in(self, target):
        self.anim_opacity_out.stop(target)
        self.anim_opacity_in.start(target)

    def opacity_out(self, target):
        self.anim_opacity_in.stop(target)
        self.anim_opacity_out.start(target)

    def on_connected(self, *args):
        if self.connected:
            self.opacity_out(self.ids.connection_layout)
        else:
            self.opacity_in(self.ids.connection_layout)

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
        if self.loading or self.ids.connection_button.disabled:
            return
        self.loading = True
        Clock.schedule_once(self.start_connection, 0.5)

    def start_connection(self, *args):
        def on_succes():
            Clock.schedule_once(self.toogle_loading, 0.5)
            Info("RCM connecté")

        def on_error(e):
            def c(*args):
                self.connected = True

            Clock.schedule_once(self.toogle_loading, 0.5)
            Clock.schedule_once(c, 0.5)  # TODO Remove that
            Error(str(e))

        self.client.connect(on_succes, on_error)
