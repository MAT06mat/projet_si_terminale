from kivy.uix.button import Button
from kivy.properties import ColorProperty, ListProperty
from kivy.animation import Animation
from kivy.lang import Builder


Builder.load_file("ui/button.kv")


class CustomButton(Button):
    background = ColorProperty("#E0E0E0")
    _background = ColorProperty("#E0E0E0")
    border_radius = ListProperty(None, allownone=True)
    default_radius = ListProperty([0, 0, 0, 0])

    def on_height(self, *args):
        self.default_radius = (
            self.height / 2,
            self.height / 2,
            self.height / 2,
            self.height / 2,
        )

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
