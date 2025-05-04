from kivy.properties import StringProperty
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivy.lang import Builder
from kivy.app import App
from kivy.properties import ListProperty
from kivy.core.window import Window
import os

from backend import cubeSaves, get_saves_images_path
from ui.rubiks_cube import RubiksCube
from ui.popup import BooleanPopup, TextInputPopup, Info
from imports import solver


Builder.load_file("screens/load_menu.kv")


class LoadMenu(MDFloatLayout):
    pass


class NoSaveLabel(MDLabel):
    pass


class Save(MDCard):
    name = StringProperty("No name")
    cube_string = StringProperty("")
    image_path = StringProperty("")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cube_string = cubeSaves.get(self.name)
        self.image_path = get_saves_images_path(self.cube_string)

    def load(self, *args):
        self.menu.dismiss()

        ids = App.get_running_app().root.ids
        cube: RubiksCube = ids.main_menu.ids.cube

        def on_load(rep=True):
            if rep:
                cube.from_string(self.cube_string)
                ids.screen_manager.current = "MainMenu"
                ids.main_menu_item.select()
                Info(f'Save "{self.name}" load')

        current_cube_string = cube.to_string()
        all_cube_string_save = [cubeSaves.get(key) for key in cubeSaves.keys()]
        all_cube_string_save.extend(
            [
                self.cube_string,
                solver.SOLVED_CUBE_STRING,
            ]
        )
        if current_cube_string not in all_cube_string_save:
            BooleanPopup(
                title="Cube not save !",
                text="Current cube isn't save, do you want to overwrite it ?",
                on_answer=on_load,
            )
        else:
            on_load()

    def rename(self, *args):
        self.menu.dismiss()

        def on_rename(new_name):
            if not new_name:
                return

            def _rename(rep=True):
                if rep:
                    cubeSaves.delete(self.name)
                    parent = self.parent
                    parent.remove_save(new_name)
                    parent.remove_save(self.name)
                    Info(f'Save "{self.name}" is rename to "{new_name}"')
                    self.name = new_name
                    cubeSaves.put(self.name, self.cube_string)
                    parent.add_save(self)
                    parent.check_images()

            if new_name in cubeSaves.keys():
                BooleanPopup(
                    title="Save already exist",
                    text="A save with this name already exist, do you want to overwrite it ?",
                    on_answer=_rename,
                )
            else:
                _rename()

        TextInputPopup(
            title="Raname",
            text=f'How do you want to rename "{self.name}" ?',
            default_text=self.name,
            on_answer=on_rename,
        )

    def delete(self, *args):
        self.menu.dismiss()

        def on_delete(rep):
            if rep:
                cubeSaves.delete(self.name)
                parent = self.parent
                parent.remove_save(self.name)
                parent.check_images()
                Info(f'Save "{self.name}" is deleted')

        BooleanPopup(
            title="Delete ?",
            text=f'Do you realy want to delete "{self.name}" save ?',
            on_answer=on_delete,
        )

    def on_release(self):
        if not cubeSaves.exists(self.name):
            return
        menu_items = [
            {
                "text": f"Load",
                "trailing_icon": "content-save",
                "on_release": self.load,
            },
            {
                "text": f"Rename",
                "trailing_icon": "rename",
                "on_release": self.rename,
            },
            {
                "text": f"Delete",
                "trailing_icon": "delete",
                "on_release": self.delete,
            },
        ]
        self.menu = MDDropdownMenu(caller=Window, items=menu_items, position="center")
        self.menu.open()
        return super().on_release()


class Saves(MDStackLayout):
    _saves_name = ListProperty([])
    _images: set[str] = set()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.no_save_label = NoSaveLabel()
        for name in cubeSaves.keys():
            self.add_save(name)
            self._images.add(cubeSaves.get(name))
        if len(self._saves_name) == 0:
            self.add_widget(self.no_save_label)

    @property
    def _saves(self) -> list[Save]:
        saves = []
        for children in self.children:
            if isinstance(children, Save):
                saves.append(children)
        return saves

    def add_save(self, save):
        if len(self._saves_name) == 0 and self.no_save_label.parent:
            self.remove_widget(self.no_save_label)
        new_save = None
        if isinstance(save, str):
            if save in self._saves_name:
                return
            new_save = Save(name=save)
        elif isinstance(save, Save):
            new_save = save
        self._saves_name.append(new_save.name)
        self._images.add(new_save.cube_string)
        self.add_widget(new_save)

    def remove_save(self, name):
        for save in self._saves:
            if save.name == name:
                self._saves_name.remove(name)
                self.remove_widget(save)

                if len(self._saves_name) == 0 and not self.no_save_label.parent:
                    self.add_widget(self.no_save_label)

    def check_images(self):
        _images = self._images.copy()
        for save in self._saves:
            if save.cube_string in _images:
                _images.remove(save.cube_string)

        for img in _images:
            if os.path.exists(get_saves_images_path(img)):
                self._images.remove(img)
                os.remove(get_saves_images_path(img))
