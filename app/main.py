__version__ = "0.0.1"


if __name__ == "__main__":
    from kivy.app import App
    from kivy.properties import ObjectProperty
    from kivy.core.window import Window

    from screens.navigation_screen_manager import NavigationScreenManager

    class MyScreenManager(NavigationScreenManager):
        pass

    class RubiksCubeMasterApp(App):
        manager = ObjectProperty(None)
        icon = "assets/images/logo.png"

        def build(self):
            Window.clearcolor = (1, 1, 1, 1)
            self.manager = MyScreenManager()
            return self.manager

    RubiksCubeMasterApp().run()
