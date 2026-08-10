import flet as ft
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..app import App
    
    

class Screen(ft.Stack):
    def __init__(self, app: "App"):
        super().__init__()
        self.app = app
        self.core = self.app.core
        self.expand = True
        self.main_widget = ft.Column(spacing=2)
        self.controls = [self.main_widget]
        self.build_screen()
        
        
    def build_screen(self): ...