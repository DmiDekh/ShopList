from kivymd.uix.bottomnavigation import MDBottomNavigation

from .shop_list_screen.screen import ShopListScreen


# class BottonNavigation(MDBottomNavigation):
#     def __init__(self, app, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.app = app
#         self.core = self.app.core
#         self.set_screens()
        
        
#     def set_screens(self):
#         self.add_widget(ShopListScreen(self.app))