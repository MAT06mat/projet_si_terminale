from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, BooleanProperty
from kivy.app import App
from kivy.lang import Builder

from ui.popup import TextInputPopup, BooleanPopup


Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    text = StringProperty("Logs :")
    edit_mode = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bpopup = BooleanPopup(
            title="Delete ?",
            text="Do you really want to delete that ?",
        )
        self.bpopup.bind(answer=self.new_answer)
        self.tpopup = TextInputPopup(title="Save name")
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
