from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import StringProperty, BooleanProperty
from kivy.lang import Builder

from ui.popup import InputPopup, BooleanPopup


Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    text = StringProperty("Logs :")
    edit_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bpopup = BooleanPopup(title="Delete ?", yes_button_color="#FB7B62")
        self.bpopup.bind(answer=self.new_answer)
        self.tpopup = InputPopup(
            title="Save name",
        )
        self.tpopup.bind(answer=self.new_answer)
        self.dropmenu = None

    def new_answer(self, popup, answer):
        self.log(answer)

    def log(self, text):
        self.text += f"\n{text}"

    def reset_logs(self):
        self.text = "Logs :"
        self.dropmenu.dismiss()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

    def open_menu(self):
        if not self.dropmenu:
            menu_items = [
                {
                    "text": "Save cube",
                    "leading_icon": "content-save",
                    "on_release": self.save_cube,
                },
                {
                    "text": "Load cube",
                    "leading_icon": "content-save-edit",
                    "on_release": self.load_cube,
                },
                {
                    "text": "Connect bluetooth",
                    "leading_icon": "bluetooth",
                    "on_release": self.connect_bluetooth,
                },
                {
                    "text": "Reset logs",
                    "leading_icon": "reload",
                    "on_release": self.reset_logs,
                },
            ]
            self.dropmenu = MDDropdownMenu(
                caller=self.ids.menu_button, items=menu_items
            )
        self.dropmenu.open()

    def save_cube(self):
        self.log("Cube saved !")
        self.dropmenu.dismiss()

    def load_cube(self):
        self.log("Cube loaded !")
        self.dropmenu.dismiss()

    def connect_bluetooth(self):
        self.log("Bluetooth connected !")
        self.dropmenu.dismiss()
