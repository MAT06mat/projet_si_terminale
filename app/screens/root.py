from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.dialog import MDDialog
from kivy.properties import BooleanProperty


class NavigationDrawerItem(MDNavigationDrawerItem):
    selectable = BooleanProperty(True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(selected=self.select)

    def select(self, *args):
        if self.selected:
            self._drawer_menu.update_items_color(self)

    def on_release(self, *args):
        if self.selectable:
            return super().on_release(*args)


class Dialog(MDDialog):
    pass


class Root(MDScreen):
    def push(self, screen):
        self.ids.screen_manager.current = screen
        self.ids.nav_drawer.set_state("toggle")

    def save_cube(self):
        Dialog().open()
