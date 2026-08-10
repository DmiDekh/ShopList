from .config import *


from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager

from core.core import Core

from .screens import ShopListScreen



class ShopListApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "DeepPurple"
        self.core = Core(self)
        
        sm = MDScreenManager()
        
        sm.add_widget(ShopListScreen(name="shop_list"))
        
        return sm
    

