__version__ = "0.0.0"

if __name__ == "__main__":
    from kivy.app import App
    from kivy.properties import ObjectProperty
    from screens.navigation_screen_manager import NavigationScreenManager

    class MyScreenManager(NavigationScreenManager):
        pass

    class RubiksCubeMasterApp(App):
        manager = ObjectProperty(None)
        icon = "assets/images/app/logo.png"

        def build(self):
            self.manager = MyScreenManager()
            return self.manager

    RubiksCubeMasterApp().run()
