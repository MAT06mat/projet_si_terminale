from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from ui.popup import Error
from backend import bluetoothClient

Builder.load_file("screens/bluetooth/connected.kv")


class BluetoothConnectedScreen(MDBoxLayout):
    manager = ObjectProperty(None)
    menu = ObjectProperty(None)

    def scan_cube(self):
        print("Scan cube")

    def solve_cube(self):
        menu_items = [
            {
                "text": f"From scan",
                "trailing_icon": "cube-scan",
                "on_release": self.solve_cube_from_scan,
            },
            {
                "text": f"From app",
                "trailing_icon": "cube-outline",
                "on_release": self.solve_cube_from_app,
            },
            {
                "text": f"From save",
                "trailing_icon": "content-save",
                "on_release": self.solve_cube_from_save,
            },
        ]
        self.menu = MDDropdownMenu(caller=self, items=menu_items, position="center")
        self.menu.open()

    def solve_cube_from_scan(self):
        if isinstance(self.menu, MDDropdownMenu):
            self.menu.dismiss()

    def solve_cube_from_app(self):
        if isinstance(self.menu, MDDropdownMenu):
            self.menu.dismiss()

    def solve_cube_from_save(self):
        if isinstance(self.menu, MDDropdownMenu):
            self.menu.dismiss()

    def randomize_cube(self):
        print("Randomize cube")
