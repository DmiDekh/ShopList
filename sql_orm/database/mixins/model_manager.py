from typing import TYPE_CHECKING

from .base import *
from ...tools import *
from ...fields import *
if TYPE_CHECKING:
    from ...model import Model
    
    
type ModelCls = type[Model]


class ModelManagerMixin(BaseMixin):
    def register_model(self, mcls: ModelCls):
        mcls._table_name = mcls.__name__.lower()
        columns_def = [f.as_column_def() for f in mcls._fields.values()]
        columns_def.insert(0, "id INTEGER PRIMARY KEY AUTOINCREMENT")
        self.create_table(mcls._table_name, columns_def)
        mcls._db = self
        
        
    # ======= Decorator
    def register(self):
        def decorator(mcls):
            self.register_model(mcls)
            return mcls
        return decorator