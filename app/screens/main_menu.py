from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder

from ui.popup import InputPopup, BooleanPopup


Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    text = StringProperty("Logs :")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bpopup = BooleanPopup(title="Delete ?", yes_button_color="#FB7B62")
        self.bpopup.bind(answer=self.new_answer)
        self.tpopup = InputPopup(
            title="Save name",
        )
        self.tpopup.bind(answer=self.new_answer)

    def new_answer(self, popup, answer):
        self.log(answer)

    def log(self, text):
        self.text += f"\n{text}"
