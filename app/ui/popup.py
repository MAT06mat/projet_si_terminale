from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import (
    StringProperty,
    ColorProperty,
    BooleanProperty,
    NumericProperty,
    ObjectProperty,
)
from kivy.lang import Builder


Builder.load_file("ui/popup.kv")


class CustomPopup(Popup):
    @property
    def label(self) -> Label:
        return self.children[0].children[-1]

    answer = BooleanProperty(None, force_dispatch=True)
    _pre_answer = False

    def on_dismiss(self, *args):
        self.answer = self._pre_answer
        self._pre_answer = False

    def on_validate(self, answer):
        self._pre_answer = answer
        self.dismiss()


class BooleanPopup(CustomPopup):
    yes_button_text = StringProperty("Yes")
    no_button_text = StringProperty("No")

    yes_button_color = ColorProperty("#E0E0E0")
    no_button_color = ColorProperty("#E0E0E0")


class InputPopup(CustomPopup):
    max_characters = NumericProperty(99)
    input_filter = ObjectProperty(None)

    @property
    def text_input(self, *args) -> TextInput:
        return self.ids["input"]

    def open(self, *_args, **kwargs):
        self.text_input.focus = True
        self.text_input.text = ""
        return super().open(*_args, **kwargs)
