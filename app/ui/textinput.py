from kivy.uix.textinput import TextInput
from kivy.properties import NumericProperty


class LimitedTextInput(TextInput):
    max_characters = NumericProperty(99)

    def on_text(self, *args):
        if len(self.text) > self.max_characters:
            self.text = self.text[: self.max_characters]
