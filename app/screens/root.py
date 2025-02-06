from kivymd.uix.screen import MDScreen


class Root(MDScreen):
    def push(self, screen):
        self.ids.screen_manager.current = screen
        self.ids.nav_drawer.set_state("toggle")
