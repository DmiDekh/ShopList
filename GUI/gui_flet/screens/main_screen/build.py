import flet as ft
from typing import TYPE_CHECKING

from ..screen import Screen


from core.models import Item, Store, Order, CatalogItem

if TYPE_CHECKING:
    from .main_screen import MainScreen
    
    
from .views import StoreOrderView

class Build(Screen):
    _views: dict[Store | None, "StoreOrderView"] = {}
        
    def build_screen(self: "MainScreen"):
        # ================== Store ====
        self.store_text_field = ft.TextField(
            label="Название магазина", 
            on_change=self.c_show_store_hints,
            height=50)
        
        self.store_hints = ft.ListView(
            spacing=1,
            visible=False,
            top=50, left=0, right=0)
        
        button_clear_store_text_field = ft.IconButton(
            icon=ft.Icons.CLEAR,
            icon_color=ft.Colors.RED,
            on_click=self.c_clear_store_text_field,
            width=50, height=50)
        
        store_row = ft.Row(
            controls=[self.store_text_field, button_clear_store_text_field],
            spacing=2)
        
        # ============= Item Row ===============
        self.item_text_field = ft.TextField(
            label="Название продукта",
            on_change=self.c_show_item_hints,
            on_submit=self.c_add_order)
        
        self.item_hints = ft.ListView(
            spacing=1,
            visible=False,
            top=102, left=0, right=0)
        
        button_add_shopping_item = ft.IconButton(
            icon=ft.Icons.ADD_SHOPPING_CART,
            icon_color=ft.Colors.GREEN,
            on_click=self.c_add_order, 
            width=50, height=50)
        
        item_row = ft.Row(
            controls=[self.item_text_field, button_add_shopping_item],
            spacing=2
        )
        
        # =============== Scroll Widget ================
        self.scroll_widget = ft.Column(
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=4)
        
        
        self.main_widget.controls = [store_row, item_row, self.scroll_widget]
        self.controls.append(self.store_hints)
        self.controls.append(self.item_hints)
        
        
        for order in Order.get_all():
            self.add_order(order)
            
        # for store_list in self.core.store_shopping_lists:
        #     self.scroll_widget.controls.append(
        #         StoreShoppingListView(store_list, lambda e: print(f"delete {e}"))
        #     )
        
        
    # def getShoppingItemView(self: "MainScreen", item):
    #     return ShoppingItemView(item, self.callback_delete_shopping_item_view)
    
        
    def add_order(self, order: Order):
        if (view := self._views.get(order.store)) is not None:
            view.add_order(order)
        else:
            i = self._views[order.store] = StoreOrderView(order=order, on_delete=self.on_delete_store_order)
            self.scroll_widget.controls.append(i)
            
            
    def on_delete_store_order(self, sov: StoreOrderView):
        self.scroll_widget.controls.remove(sov)
        