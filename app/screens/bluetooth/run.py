from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import ObjectProperty
from kivy.lang import Builder

Builder.load_file("screens/bluetooth/run.kv")


class BluetoothRunScreen(MDBoxLayout):
    manager = ObjectProperty(None)
