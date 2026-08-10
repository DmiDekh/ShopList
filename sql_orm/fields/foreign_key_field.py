from typing import Callable, Any, TYPE_CHECKING
from dataclasses import dataclass, field

from .base import Field, SQLType, UNSET


if TYPE_CHECKING:
    from ..model import Model
    
    
@dataclass
class ForeignKeyField(Field["Model"]):
    model: "Model" = None
    types: type | tuple[type] = field(default=int, init=False)
    default: Any = field(default=UNSET, init=False)
    factory: Callable[..., Any] = field(default=UNSET, init=False)
    serialize: Callable = field(default=None, init=False)
    deserialize: Callable[..., Any] = field(default=None, init=False)
    converter: Callable[..., Any] = field(default=None, init=False)
    validate_value: Callable[..., Any] = field(default=None, init=False)
    sql_type: SQLType = field(default=SQLType.INTEGER, init=False)
    unique: bool = field(default=False, init=False)
    
    
    def __post_init__(self):
        # if not any(o.__name__ == "Model" for o in self.model.__mro__):
        #     raise
        return super().__post_init__()
    
        
    def __get__(self, ins, owner):
        if ins is None: return self
        id = getattr(ins, self.storage_name)
        return self.model.get_by_id(id) if id is not None else None
    
    
    
    @staticmethod
    def field_serialize(value):
        return value.id if value else None
    
    
    @staticmethod
    def field_converter(value):
        return value.id
    
    
    
ForeignKeyField()