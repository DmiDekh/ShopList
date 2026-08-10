import flet as ft
from core.models import Item, Store, Order, CatalogItem, OrderState
from core import Core




    
    

class StoreOrderView(ft.Container):
    _stores: dict[str, Store]
    
    
    def __init__(self, order: Order, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.order = order
        self.on_delete = on_delete
        
        store_but = ft.Button(
            content= ft.Text(self.order.store.name if self.order.store else "Общий список", size=28), 
                              height=50, expand=True, on_click=self.toggle_vis_orders)
        store_del = ft.IconButton(icon= ft.Icons.DELETE_OUTLINE, icon_color= ft.Colors.RED, on_click=self.del_self)
        self.orders_col = ft.Column()
        self.content = ft.Column(controls= [ft.Row(controls=[store_but, store_del]), self.orders_col])
        self.bgcolor = ft.Colors.GREY_300
        self.border_radius = 5
        self.border=ft.Border.all(3, ft.Colors.GREY_400)
        self.add_order(order)
        
        
    def add_order(self, order: Order):
        self.orders_col.controls.append(OrderView(order, on_delete=self.del_order))
        
        
    def toggle_vis_orders(self, e):
        self.orders_col.visible = not self.orders_col.visible
        
        
    def del_self(self, e):
        for ov in self.orders_col.controls:
            ov.order.delete()
        self.on_delete(self)
        
        
    def del_order(self, ov: "OrderView"):
        ov.order.delete()
        self.orders_col.controls.remove(ov)
        self.update()
        
    
        
        
        
        
        
class OrderView(ft.Row):
    _text_styles = {
        OrderState.ACTIVE: ft.TextStyle(decoration=ft.TextDecoration.NONE, color=None),
        OrderState.IN_CART: ft.TextStyle(decoration=ft.TextDecoration.NONE, color=ft.Colors.GREEN),
        OrderState.BOUGHT: ft.TextStyle(decoration=ft.TextDecoration.LINE_THROUGH, color=ft.Colors.GREY, decoration_thickness=2.5),
    }
    def __init__(self, order: Order, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.order = order
        self.on_delete = on_delete
        
        self.setup_self()
        self.create_childs()
        
        
    def setup_self(self):
        self.spacing = 2
        
        
    def create_childs(self):
        self.text_widget = ft.Text(
            self.order.item.name,
            size=24)
        
        self.text_widget.style = self._text_styles[self.order.state]
        
        self.text_button = ft.Button(
            content = self.text_widget, 
            expand = True, 
            height=40,
            on_click = self.call_buy_item)
        
        self.cart_button = ft.IconButton(
            icon = ft.Icons.SHOPPING_CART,
            icon_color = ft.Colors.GREY,
            on_click= self.call_in_cart_item)
        
        self.delete_button = ft.IconButton(
            icon= ft.Icons.DELETE_OUTLINE,
            icon_color= ft.Colors.RED,
            on_click=lambda e: self.on_delete(self))
        
        self.controls = [self.text_button, self.cart_button, self.delete_button]
        
        
    def call_in_cart_item(self, e):
        if self.order.state is OrderState.ACTIVE:
            self.order.mark_as_in_cart()
            self.cart_button.icon_color = ft.Colors.GREEN
        elif self.order.state is OrderState.IN_CART:
            self.order.mark_as_active()
            self.cart_button.icon_color = ft.Colors.GREY
        self.text_widget.style = self._text_styles[self.order.state]
        self.update()
            
            
    def call_buy_item(self, e):
        if self.order.state is OrderState.ACTIVE or self.order.state is OrderState.IN_CART:
            self.order.mark_as_bought()
            self.cart_button.icon_color = ft.Colors.GREY
        elif self.order.state is OrderState.BOUGHT:
            self.order.mark_as_active()
        self.text_widget.style = self._text_styles[self.order.state]
        self.update()




# class StoreShoppingListView(ft.Container):
#     def __init__(self, item: StoreShoppingList, on_delete):
#         super().__init__()
#         self.item = item
#         self.on_delete = on_delete
#         text = ft.Text(item.store.name, size=24, expand=True)
#         delete_button = ft.IconButton(icon=ft.Icons.DELETE_OUTLINE)
#         self.bgcolor = ft.Colors.GREY
        
#         self.column = ft.Column(
#             controls=[ft.Row(controls=[text, delete_button])]
#         )
#         self.content = self.column
        
#         self.store_name = self.item.store.name
#         for i in self.item.items:
#             self.add_shopping_item(i)
        
#     def add_shopping_item(self, item: ShoppingItem):
#         self.column.controls.append(
#             ft.Row(controls=[
#                 ft.Container(width=30),
#                 ShoppingItemView(item, on_delete=self.delete_shopping_item, expand=True)
#             ])
#         )
        
#     def delete_shopping_item(self, e): ...