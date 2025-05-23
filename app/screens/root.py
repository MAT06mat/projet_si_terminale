from kivymd.uix.screen import MDScreen
from kivymd.uix.navigationdrawer import MDNavigationDrawerItem
from kivymd.uix.dialog import MDDialog
from kivy.properties import BooleanProperty

from ui.popup import TextInputPopup, BooleanPopup, Info, Error
from ui.rubiks_cube import RubiksCube
from imports import solver
from backend import cubeSaves, get_saves_images_path


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
        if screen == "Settings":
            Error("[Error 666] Une anomalie démoniaque a corrompu le système.")
        self.toggle_drawer()

    def toggle_drawer(self):
        self.ids.nav_drawer.set_state("toggle")

    @property
    def cube(self) -> RubiksCube:
        return self.ids.main_menu.ids.cube

    def save_cube(self):
        def on_save(save_name):
            if not save_name:
                return

            def _save(rep=True):
                if rep:
                    cube_string = self.cube.to_string()
                    cubeSaves.put(save_name, cube_string)
                    image_path = get_saves_images_path(cube_string)
                    self.cube.export_to_png(image_path)
                    self.ids.load_menu.ids.saves.add_save(save_name)
                    Info(f'Cube successfully saved at "{save_name}"')

            if cubeSaves.exists(save_name):
                BooleanPopup(
                    title=f'Save "{save_name}" already exist, do you want to overwrite it ?',
                    text="This action cannot be reversed",
                    on_answer=_save,
                )
            else:
                _save()

        TextInputPopup(title="Save name", on_answer=on_save)

    def delete_cube(self):
        if self.cube.is_solve():
            return

        def on_delete(rep):
            if rep:
                self.cube.from_string(solver.SOLVED_CUBE_STRING)

        BooleanPopup(
            title="Delete ?",
            text="Do you realy want to delete ths cube ?",
            on_answer=on_delete,
        )
