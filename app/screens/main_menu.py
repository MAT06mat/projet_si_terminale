from kivymd.uix.boxlayout import BoxLayout
from kivy.properties import BooleanProperty
from kivy.app import App
from kivy.lang import Builder

Builder.load_file("screens/main_menu.kv")


class MainMenu(BoxLayout):
    edit_mode = BooleanProperty(False)

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode

    def togle_menu(self):
        app = App.get_running_app()
        app.root.ids.nav_drawer.set_state("toggle")
