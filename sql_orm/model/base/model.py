from typing import TYPE_CHECKING, Self, dataclass_transform

from .metaclass_model import MetaclassModel

from ...fields import *
from ...tools import *

from ..mixins import DatabaseMethodsMixin


if TYPE_CHECKING:
    from ...database import Database
    

@dataclass_transform(
kw_only_default=True,
# Указываем Pylance, какие классы считаются описателями полей
field_specifiers=(Field, StrField, IntField, DatetimeField, ForeignKeyField))
class Model(DatabaseMethodsMixin,
    metaclass=MetaclassModel):
    _fields: dict[str, Field]
    _table_name: TableName = None
    _db: "Database" = None
    _id: int | None = None
    
    def __init_subclass__(cls):
        cls._cache: dict[ID, "Model"] = {}
        return cls
    
    
    def __init__(self, **kwargs):
        self.auto_save: bool = False
        for field_name in self._fields.keys():
            setattr(self, field_name, kwargs.get(field_name, UNSET))
        self.auto_save = True
        self.__post_init__()
        
    def __post_init__(self): pass
    
    
            
            
    def __str__(self):
        return f"{self.__class__.__name__}({", ".join(f"{f_name} = {getattr(self, f_name)}" for f_name in self._fields.keys())})"
    __repr__ = __str__
            
    @property
    def id(self):
        return self._id
    
    
    def to_dict(self, serialize: bool = False, with_id: bool = False) -> DataDict:
        if serialize:
            data = {field_name: field.serialize(getattr(self, field_name)) for field_name, field in self._fields.items()}
        else:
            data = {field_name: getattr(self, field_name) for field_name in self._fields.keys()}
        return {"id": self.id, **data} if with_id else data
    
    
    @classmethod
    def from_dict(cls, data: QueryDict) -> Self:
        deserialize_data = {field_name: field.deserialize(data.get(field_name)) for field_name, field in cls._fields.items()}
        ins = cls(**deserialize_data)
        ins._id = data["id"]
        cls._cache[ins.id] = ins
        return ins
        
        
    