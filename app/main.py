__version__ = "0.0.5"


if __name__ == "__main__":
    from kivymd.app import MDApp
    from kivymd.theming import ThemeManager
    from kivy.properties import ObjectProperty
    from kivy.metrics import sp
    from kivy.core.text import LabelBase
    from screens.root import Root

    class RubiksCubeMasterApp(MDApp):
        root = ObjectProperty(None)
        icon = "assets/images/logo.png"

        def build(self):
            self.theme_cls: ThemeManager
            self.theme_cls.theme_style = "Light"
            self.theme_cls.primary_palette = "Blue"
            LabelBase.register(
                name="lalezar",
                fn_regular="assets/fonts/Lalezar-Regular.ttf",
            )

            self.theme_cls.font_styles["lalezar"] = {
                "large": {
                    "line-height": 1,
                    "font-name": "lalezar",
                    "font-size": sp(25),
                },
                "medium": {
                    "line-height": 0.8,
                    "font-name": "lalezar",
                    "font-size": sp(20),
                },
                "small": {
                    "line-height": 0.8,
                    "font-name": "lalezar",
                    "font-size": sp(15),
                },
            }
            self.root = Root()
            return self.root

    RubiksCubeMasterApp().run()
