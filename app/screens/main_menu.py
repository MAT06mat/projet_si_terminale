from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import App
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
        self.togle_menu()

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

    def togle_menu(self):
        app = App.get_running_app()
        app.root.ids.nav_drawer.set_state("toggle")

    def save_cube(self):
        self.log("Cube saved !")
        self.togle_menu()

    def load_cube(self):
        self.log("Cube loaded !")
        self.togle_menu()

    def connect_bluetooth(self):
        self.log("Bluetooth connected !")
        self.togle_menu()
