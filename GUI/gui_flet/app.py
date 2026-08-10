import flet as ft

from core import Core
from .screens import SN, MainScreen
    
    

class App:
    resolution = (400, 700)
    
    def __init__(self, core):
        self.core: Core = core
        self.set_screens()
        
        
    def set_screens(self):
        self.screens = {}
        self.screens[SN.MAIN] = MainScreen(self)
        #self.screens[SN.SETTINGS] = SettingsScreen(self)
        
        
    def run(self):
        ft.app(target=self.launch)
        
        
    def web_run(self):
        ft.app(target=self.launch, view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=2004)
        
        
    def launch(self, page: ft.Page):
        self.page = page
        self.page.title = "Список покупок"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.window.width = self.resolution[0]
        self.page.window.height = self.resolution[1]
        self.page.padding = 0
        

        self.page.on_route_change = self.route_change
        
        self.route_change(self.page.route)
        
        
    def route_change(self, route):
        """Аналог ScreenManager: выбирает экран на основе пути (route)"""
        self.page.views.clear()
        page = self.screens.get(self.page.route)
        self.page.views.append(ft.View(route = self.page.route, controls = [page]))
        self.page.update()

