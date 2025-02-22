from kivy.properties import StringProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDListItem
from kivy.lang import Builder
from kivy.app import App


from backend import cubeSaves
from ui.rubiks_cube import RubiksCube
from ui.popup import BooleanPopup, TextInputPopup, Info
from imports import solver


Builder.load_file("screens/load_menu.kv")


class LoadMenu(MDBoxLayout):
    pass


class Saves(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in cubeSaves.keys():
            self.add_save(name)

    def add_save(self, name):
        self.add_widget(Save(name=name))

    def remove_save(self, name):
        for children in self.children:
            if isinstance(children, Save):
                if children.name == name:
                    self.remove_widget(children)


class Save(MDListItem):
    name = StringProperty("No name")

    def load(self, *args):
        self.menu.dismiss()

        ids = App.get_running_app().root.ids
        new_cube_string = cubeSaves.get(self.name)
        cube: RubiksCube = ids.main_menu.ids.cube

        def on_load(rep=True):
            if rep:
                cube.from_string(new_cube_string)
                ids.screen_manager.current = "MainMenu"
                ids.main_menu_item.select()
                Info(f'Save "{self.name}" load')

        current_cube_string = cube.to_string()
        all_cube_string_save = [cubeSaves.get(key) for key in cubeSaves.keys()]
        all_cube_string_save.extend(
            [
                new_cube_string,
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
            def _rename(rep=True):
                if rep:
                    cube_string = cubeSaves.get(self.name)
                    cubeSaves.delete(self.name)
                    parent = self.parent
                    parent.remove_save(new_name)
                    parent.remove_save(self.name)
                    Info(f'Save "{self.name}" is rename to "{new_name}"')
                    self.name = new_name
                    cubeSaves.put(self.name, cube_string)
                    parent.add_widget(self)

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
            on_answer=on_rename,
        )

    def delete(self, *args):
        self.menu.dismiss()

        def on_delete(rep):
            if rep:
                cubeSaves.delete(self.name)
                self.parent.remove_widget(self)
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
        self.menu = MDDropdownMenu(caller=self, items=menu_items, position="center")
        self.menu.open()
        return super().on_release()
