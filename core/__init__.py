from .models import *




class Core:
    def __init__(self):
        db = Database("ShopList.db")
        for i in (Item, Store, Order, CatalogItem):
            db.register_model(i)
            
            
        Store.get_or_create(name="Шериф")
        Store.get_or_create(name="Благода")
            
        
        