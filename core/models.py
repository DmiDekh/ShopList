from sql_orm.SQL import *

from datetime import datetime
from enum import StrEnum


class Item(Model):
    name: str = StrField(unique=True)
    
    
class Store(Model):
    name: str = StrField(unique=True)
    catalog: "Catalog"
    
    def __post_init__(self):
            self.catalog = Catalog(self)

class CatalogItem(Model):
    item: Item = ForeignKeyField(model=Item)
    store: Store = ForeignKeyField(model=Store)
    price: float = FloatField()
    amount: int = IntField(default=1, allow_none=True)
    weight: float = FloatField(default=None, allow_none=True)

class Catalog:
    def __init__(self, store: "Store"):
        self.store = store
        self.db = self.store._db
        
        
    def get(self, item: "Item") -> CatalogItem | None:
        return CatalogItem.get(item=item)

    
    
    
class OrderState(StrEnum):
    ACTIVE = "active"
    IN_CART = "in_cart"
    BOUGHT = "bought"
    OUT_OF_STOCK = "out_of_stock"
    
    
class Order(Model):
    item: Item = ForeignKeyField(model=Item)
    store: Store | None = ForeignKeyField(model=Store, allow_none=True)
    quantity: int = IntField(default=1)
    state: OrderState = Field(types=OrderState, default=OrderState.ACTIVE, 
                              serialize=lambda v: v.value, deserialize=lambda v: OrderState(v))
    created_at: datetime = DatetimeField(factory=datetime.now)
    
    
    def mark_as_active(self): self.state = OrderState.ACTIVE
    def mark_as_in_cart(self): self.state = OrderState.IN_CART
    def mark_as_bought(self): self.state = OrderState.BOUGHT

    
    
    