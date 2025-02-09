from kivymd.uix.textfield import MDTextField
from kivy.properties import NumericProperty


class LimitedTextInput(MDTextField):
    max_characters = NumericProperty(99)

    def set_text(self, instance, text):
        if len(text) > self.max_characters:
            text = text[: self.max_characters]
        return super().set_text(instance, text)
