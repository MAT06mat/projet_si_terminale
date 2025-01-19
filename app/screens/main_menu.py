from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))


Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    text = StringProperty("Logs :")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.test1, 3)

    def test1(self, *args):
        self.text += "\n-> test 1"
        try:
            from bluetooth import Client, Request

            self.text += "\ntest passed"
        except Exception as e:
            self.text += f"\n{e}"

    def test2(self, *args):
        pass

    def test3(self, *args):
        pass

    def test4(self, *args):
        pass
