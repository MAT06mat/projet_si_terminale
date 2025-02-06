from kivymd.uix.appbar import MDTopAppBar
from kivy.properties import StringProperty
from kivy.lang import Builder


Builder.load_file("ui/backAppBar.kv")


class BackAppBar(MDTopAppBar):
    title = StringProperty("No title")
