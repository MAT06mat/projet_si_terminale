from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty
from kivy.lang import Builder


Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    text = StringProperty("Logs :")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.text += f"\ntry start"
        try:
            from imports import bluetooth_socket as bs

            client = bs.Client("00:1a:7d:da:71:15")
            client.connect()
            self.text += f"\ntry end"
        except Exception as e:
            self.text += f"\nexception : {e}"
