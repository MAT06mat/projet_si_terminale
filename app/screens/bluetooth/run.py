from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty, StringProperty
from kivy.lang import Builder

Builder.load_file("screens/bluetooth/run.kv")


class BluetoothRunScreen(MDBoxLayout):
    manager = ObjectProperty(None)
    title = StringProperty("No title")
