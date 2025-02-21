from kivymd.uix.dialog import MDDialog
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivymd.uix.snackbar import MDSnackbar
from kivy.properties import (
    StringProperty,
    ColorProperty,
    BooleanProperty,
    NumericProperty,
    StringProperty,
)
from kivy.lang import Builder


Builder.load_file("ui/popup.kv")


class CustomPopup(MDDialog):
    title = StringProperty("No title")
    text = StringProperty("")

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

    yes_button_color = ColorProperty(None, allownone=True)
    no_button_color = ColorProperty(None, allownone=True)


class TextInputPopup(CustomPopup):
    max_characters = NumericProperty(99)

    @property
    def text_input(self, *args) -> TextInput:
        return self.ids["text_input"]

    def open(self, *_args, **kwargs):
        self.text_input.focus = True
        self.text_input.text = ""
        return super().open(*_args, **kwargs)


class Error(MDSnackbar):
    text = StringProperty("")
    current = None

    def __init__(self, error, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if Error.current:
            Error.current.dismiss()
        Error.current = self
        self.text = f"Error: {error}"
        self.open()
