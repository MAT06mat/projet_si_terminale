from kivymd.uix.screenmanager import ScreenManager
from kivy.properties import ListProperty
from kivy.core.window import Window


class NavigationScreenManager(ScreenManager):
    screen_stack: list = ListProperty([])

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.android_back_click)

    def android_back_click(self, window, key, *largs):
        if key == 27:
            # TODO
            return True

    def push(self, screen_name: str) -> None:
        if screen_name not in self.screen_stack:
            self.screen_stack.append(self.current)
            self.current = screen_name

    def pop(self) -> None:
        if len(self.screen_stack) <= 0:
            return
        screen_name = self.screen_stack[-1]
        del self.screen_stack[-1]
        self.current = screen_name
