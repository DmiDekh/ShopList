
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.recycleview import MDRecycleView
from kivymd.uix.list import MDList
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp
from kivymd.uix.boxlayout import MDBoxLayout



class ShopListScreen(MDBottomNavigationItem):
    def __init__(self, app, **kwargs):
        self.app = app
        self.name = self.__class__.__name__
        super().__init__(**kwargs)
        self.icon = "cart"
        self.text = "Покупки"
        sc = MDRecycleView()
        self.add_widget(sc)
        ls = MDList()
        sc.add_widget(ls)
        
        bot_add_item = MDRaisedButton(
            text="Добавить +",
            size_hint_x = 1,
            size_hint_y = None,
            height=dp(40),
        )
        bot_add_item.size_hint_x = 1
        bot_add_item.size_hint_y = None
        self.add_widget(bot_add_item)
        
        for item in self.app.core.items:
            box = MDBoxLayout(
                orientation="horizontal",
                size_hint_x=1,
                size_hint_y=None,
                height=dp(40),
                spacing=dp(5)  # Зазор между кнопками
            )
            # box.size_hint_x = None
            b_item = MDRaisedButton(
                text=item.name,
                        # Выравниваем текст по левому краю
                padding=[dp(10), 0, 0, 0]   # Отступ 10dp слева
            )
            b_item.anchor_x="left"
            # ВАЖНО: Задаем размеры ПОСЛЕ создания кнопки, 
            # чтобы переопределить внутренние KV-стили KivyMD
            b_item.size_hint_x = 1
            b_item.size_hint_y = None
            b_item.height = dp(40)
            b_item.bind(on_release=self.change_text)
            b_delete_item = MDRaisedButton(
                text="D"
            )
            b_delete_item.bind(on_release=lambda ins, ls =ls, box=box: ls.remove_widget(box))
            box.add_widget(b_item)
            box.add_widget(b_delete_item)
            ls.add_widget(box)
            
            
    def change_text(self, ins):
        if ins.text.startswith("[s]"):
            ins.text = ins.text[3:-4]
        else:
            ins.text = f"[s]{ins.text}[/s]"
            