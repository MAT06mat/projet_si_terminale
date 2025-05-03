from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.properties import BooleanProperty, ObjectProperty
from kivy.metrics import dp
from kivy.lang import Builder
from kivy.clock import Clock
from ui.popup import Error, Info

from backend import bluetoothClient

Builder.load_file("screens/bluetooth/unconnected.kv")


class BluetoothUnconnectedScreen(MDBoxLayout):
    loading = BooleanProperty(False)
    manager = ObjectProperty(None)
    text = f'[size={int(dp(25))}][b]To Connect[/b][/size]\n\nTo connect to the Rubik\'s Cube Master, turn on your RCM, enable your Bluetooth, allow the app to access Bluetooth, and click on "Connection".'

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
        if self.loading or self.ids.connection_button.disabled:
            return
        self.loading = True
        Clock.schedule_once(self.start_connection, 0.5)

    def start_connection(self, *args):
        def on_succes():
            Clock.schedule_once(self.toogle_loading, 0.5)
            self.manager.current = "connected"
            Info("RCM connected")

        def on_error(e):
            # TODO: TO ADD AND REMOVE
            # Clock.schedule_once(self.toogle_loading, 0.5)
            on_succes()
            Error(e)

        self.client.connect(on_succes, on_error)
