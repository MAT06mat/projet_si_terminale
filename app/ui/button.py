from kivy.uix.button import Button
from kivy.properties import ColorProperty
from kivy.animation import Animation
from kivy.lang import Builder


Builder.load_file("ui/button.kv")


class CustomButton(Button):
    background = ColorProperty((1, 1, 1, 1))
    _background = ColorProperty((1, 1, 1, 1))

    def on_background(self, *args):
        self._background = self.background

    def on_press(self):
        r, g, b, a = self.background
        Animation(_background=(r - 0.1, g - 0.1, b - 0.1, a), d=0.1).start(self)
        return super().on_press()

    def on_touch_up(self, touch):
        if self._background != self.background:
            Animation(_background=self.background, d=0.1).start(self)
        return super().on_touch_up(touch)
