import os
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder

kv_path = os.path.join(os.path.dirname(__file__), "screen.kv")
Builder.load_file(kv_path)



class ShopListScreen(MDScreen):
    def on_enter(self, *args):
        self.ids.container.clear_widgets()
        
        
        
    def go_to_settings(self):
        # Переключение экрана через ScreenManager
        self.manager.current = "settings"