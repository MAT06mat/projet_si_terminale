from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from ui.popup import Error
from backend import bluetoothClient

Builder.load_file("screens/bluetooth/connected.kv")


class BluetoothConnectedScreen(MDBoxLayout):
    manager = ObjectProperty(None)

    def scan_cube(self):
        print("Scan cube")

    def solve_cube(self):
        print("Solve cube")

    def randomize_cube(self):
        print("Randomize cube")

    def bluetooth_deconnect(self):
        try:
            bluetoothClient.deconnect()
        except Exception as e:
            Error(e)
        self.manager.current = "unconnected"
