from kivymd.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import NoTransition
from kivymd.uix.screen import MDScreen
from screens.bluetooth.unconnected import BluetoothUnconnectedScreen
from screens.bluetooth.connected import BluetoothConnectedScreen
from screens.bluetooth.run import BluetoothRunScreen
from kivy.clock import mainthread
from backend import bluetoothClient
from ui.popup import Error, BooleanPopup


class BluetoothScreenManager(ScreenManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.transition = NoTransition()

        screens = {
            "unconnected": BluetoothUnconnectedScreen,
            "connected": BluetoothConnectedScreen,
            "run": BluetoothRunScreen,
        }

        for name, widget in screens.items():
            screen = MDScreen(widget(manager=self), name=name)
            self.add_widget(screen)

        self.current = "unconnected"
        bluetoothClient.on_deconnect = self.on_deconnect

    @mainthread
    def on_deconnect(self):
        self.current = "unconnected"
        Error("Bluetooth connection lost")

    def bluetooth_deconnect(self):
        try:
            bluetoothClient.deconnect()
        except Exception as e:
            Error(e)
        self.current = "unconnected"

    def cancel_run(self):
        def on_answer(rep):
            if rep:
                self.current = "connected"

        BooleanPopup(
            title="Back to the app",
            text=f"This action will stop the current resolution, are you sure ?",
            on_answer=on_answer,
        )
