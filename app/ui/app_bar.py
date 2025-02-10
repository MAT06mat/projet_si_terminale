from kivymd.uix.appbar import MDTopAppBar
from kivy.properties import StringProperty
from kivy.lang import Builder


Builder.load_file("ui/app_bar.kv")


class AppBar(MDTopAppBar):
    title = StringProperty("No title")
