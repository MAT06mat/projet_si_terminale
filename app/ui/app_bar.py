from kivymd.uix.appbar import MDTopAppBar
from kivy.properties import StringProperty
from kivy.app import App
from kivy.lang import Builder


Builder.load_file("ui/app_bar.kv")


class AppBar(MDTopAppBar):
    title = StringProperty("No title")
    icon = StringProperty("menu")

    def when_button_click(self):
        App.get_running_app().root.toggle_drawer()
