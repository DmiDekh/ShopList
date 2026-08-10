from .build import *



class Callbacks(Build):
    
    def _show_hints(self, hitns_widget, text_field, names):
        def select(text):
            hitns_widget.visible = False
            text_field.value = text
            self.update()
            
        hitns_widget.visible = True
        for name in names:
            hitns_widget.controls.append(
                ft.ListTile(
                    title=ft.Text(name),
                    bgcolor=ft.Colors.GREY_100,
                    on_click=lambda e, text=name: select(text)))
        self.store_hints.update()
            
        
        
    def c_show_store_hints(self, e):
        self.store_hints.controls.clear()
        if (value := self.store_text_field.value.strip()):
            names = Store._db.find_matches(Store._table_name, ["name"], "name", value, 5)
            names = [i["name"] for i in names]
            if names:
                self._show_hints(self.store_hints, self.store_text_field, names)
            else:
                self.store_hints.visible = False
        self.store_hints.update()
        
        
    def c_show_item_hints(self, e):
        self.item_hints.controls.clear()
        if (value := self.item_text_field.value.strip()):
            names = Item._db.find_matches(Item._table_name, ["name"], "name", value, 5)
            names = [i["name"] for i in names]
            if names:
                self._show_hints(self.item_hints, self.item_text_field, names)
            else:
                self.item_hints.visible = False
        self.item_hints.update()
        
    
        
        
    def c_add_order(self, e):
        if (item_name := self.item_text_field.value.strip()):
            item = Item.get_or_create(name=item_name)
            store = Store.get_or_create(name=store_name) if (store_name := self.store_text_field.value.strip()) else None
            
            order = Order.create(item=item, store=store)
            self.add_order(order)
            self.item_text_field.value = ""
            self.store_text_field.value = ""
                    
        # if (name := self.item_text_field.value.strip()):
        #     self.item_text_field.value = ""
        #     item = self.core.create_shopping_item(name)
        #     self.scroll_widget.controls.insert(0, self.getShoppingItemView(item))
        #     self.item_hints.visible = False
        #     self.update()
            
            
    def c_delete_shopping_item_view(self, item_view): ...
        # self.core.delete_item(item_view.item)
        # self.scroll_widget.controls.remove(item_view)
        
            
    def _call_show_hints(self, text_field: ft.TextField, widget_hints: ft.ListView, names: tuple[str]): ...
        # query = text_field.value.lower().strip()
        # widget_hints.controls.clear()
        
        # if not query:
        #     widget_hints.visible = False
        #     self.update()
        #     return
        
        # matches = [name for name in names if query in name.lower()][:5]
        # if matches:
        #     def select(text):
        #         text_field.value = text
        #         widget_hints.visible = False
        #         self.update()
                
        #     widget_hints.visible = True
        #     for match in matches:
        #         widget_hints.controls.append(
        #             ft.ListTile(
        #                 title=ft.Text(match),
        #                 bgcolor=ft.Colors.GREY_100,
        #                 on_click=lambda e, text=match: select(text)))
        # else:
        #     widget_hints.visible = False
        #     self.update()
                    
                
                
                
    def c_select_item_hint(self, text): ...
        # self.item_text_field.value = text
        # self.item_hints.visible = False
        # self.update()
        
        
    # def c_show_store_hints(self, e):
    #     self._call_show_hints(self.store_text_field, self.store_hints, self.store_names)
        
    # def c_show_item_hints(self, e):
    #     self._call_show_hints(self.item_text_field, self.item_hints, self.item_names)
    
    
    def c_clear_store_text_field(self, e):
        self.store_text_field.value = ""