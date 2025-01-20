from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.clock import Clock
from kivy.lang import Builder


Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    text = StringProperty("Logs :")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.test, 3)

    def test(self, *args):
        self.text += "\n-> test"
        try:
            from bluetooth import Client

            client = Client("b4:8c:9d:51:83:76", 4)
            state = client.connect()

            self.text += f"\nconnection = {str(state)}"

            self.text += "\ntest passed"
        except Exception as e:
            self.text += f"\n{e}"
