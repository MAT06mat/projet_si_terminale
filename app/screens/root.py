from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.dialog import MDDialog
from kivy.properties import BooleanProperty

from ui.popup import TextInputPopup, BooleanPopup, Info
from ui.rubiks_cube import RubiksCube
from backend import cubeSaves


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
        self.toggle_drawer()

    def toggle_drawer(self):
        self.ids.nav_drawer.set_state("toggle")

    def save_cube(self):
        self.toggle_drawer()
        popup = TextInputPopup(title="Save name")
        popup.bind(answer=self.on_save)
        popup.open()

    def on_save(self, popup, save_name):
        if not save_name:
            return

        def save(rep=True):
            if not rep:
                return
            cube: RubiksCube = self.ids.main_menu.ids.cube
            cubeSaves.put(save_name, cube.to_string())
            self.ids.main_menu.log("New save at '%s'" % save_name)
            Info(f'Cube successfully saved at "{save_name}"')

        if cubeSaves.exists(save_name):
            BooleanPopup(
                title=f'Save "{save_name}" already exist, do you want to overwrite it ?',
                text="This action cannot be reversed",
                on_answer=save,
            ).open()
            self.ids.main_menu.log("Save '%s' already exist" % save_name)
        else:
            save()
