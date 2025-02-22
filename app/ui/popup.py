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

    def __init__(
        self, title="No title", text="", on_answer=None, auto_open=True, *args, **kwargs
    ):
        super().__init__(title=title, text=text, *args, **kwargs)
        self.on_answer = on_answer
        if auto_open:
            self.open()

    def on_dismiss(self, *args):
        self.answer = self._pre_answer
        if self.on_answer:
            self.on_answer(self.answer)
        self._pre_answer = False

    def on_validate(self, answer):
        self._pre_answer = answer
        self.dismiss()


class BooleanPopup(CustomPopup):
    yes_button_text = StringProperty("Yes")
    no_button_text = StringProperty("No")

    yes_button_color = ColorProperty("#FB7B62", allownone=True)
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


class CustomSnackbar(MDSnackbar):
    text = StringProperty("")
    text_color = None
    current = None

    def __init__(self, text: str, *args, **kwargs):
        super().__init__(text=text, *args, **kwargs)
        if CustomSnackbar.current:
            CustomSnackbar.current.dismiss()
        CustomSnackbar.current = self
        self.open()


class Info(CustomSnackbar):
    pass


class Error(CustomSnackbar):
    text_color = ColorProperty((0, 0, 0, 1))

    def __init__(self, text: str, *args, **kwargs):
        super().__init__(text, *args, **kwargs)
        self.text_color = self.theme_cls.errorColor
        self.text = f"Error: {text}"
