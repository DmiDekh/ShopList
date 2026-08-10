from typing import Generic, TypeVar, Callable, TYPE_CHECKING, Any
from dataclasses import dataclass

from ...tools import *


if TYPE_CHECKING:
    from ...model import Model

T = TypeVar("T")



@dataclass
class Field(Generic[T]):
    types: type | tuple[type] = (object, )
    default: Any = UNSET
    factory: Callable = UNSET
    allow_none: bool = False
    converter: Callable = None
    validate_value: Callable = None
    serialize: Callable = None
    deserialize: Callable = None
    sql_type: SQLType = SQLType.TEXT
    unique: bool = False
    
    
    def __post_init__(self):
        self.types = TE.extract(self.types)
        
        self.converter      = self.converter      or self.__class__.field_converter
        self.validate_value = self.validate_value or self.__class__.field_validate_value
        self.serialize      = self.serialize      or self.__class__.field_serialize
        self.deserialize    = self.deserialize    or self.__class__.field_deserialize
        
        
    # ============ DECORATOR
    def __set_name__(self, owner: type["Model"], name):
        self.field_name = name
        self.storage_name = f"_{name}"
        if self.types == (object, ):
            self.get_type_from_annotations(owner)
        self._update_types()
                
        
    def __get__(self, ins: "Model", owner: type["Model"]) -> T:
        if ins is None:
            return self
        if (value := getattr(ins, self.storage_name, UNSET)) is not UNSET:
            return value
        if (value := self.get_default()) is not UNSET:
            return value
        raise "No value"
    
    
    def __set__(self, ins: "Model", value: T):
        if value is UNSET:
            if (value := self.get_default()) is UNSET:
                raise "Field is Required"
        else:
            value = self.validate(value)
        setattr(ins, self.storage_name, value)
        ins._update_by_field(self)
        
    # =========== VALIDATION
    def validate(self, value: Any) -> T:
        if not isinstance(value, self.types):
            value = self.converter(value)
            if not isinstance(value, self.types):
                raise "Convert Error"
        return self.validate_value(value)
    
    
    @staticmethod
    def field_converter(value):
        raise TypeError(f"{value},")
    
    @staticmethod
    def field_validate_value(value):
        return value
    
    
    # ============ DEFAULT
    def get_default(self) -> T | Unset:
        if self.default is not UNSET: return self.default
        if self.factory is not UNSET: return self.factory()
        if self.allow_none: return None
        return UNSET
    
    
    # ========= SQL Codec
    @staticmethod
    def field_serialize(value: T) -> SQLType:
        return value
    
    @staticmethod
    def field_deserialize(value: SQLType) -> T:
        return value
    
    
    # ========= HELP METHODS
    def as_column_def(self) -> ColumnDef:
        return " ".join(filter(None, (
            self.field_name, self.sql_type.name,
            "UNIQUE" if self.unique else None,
            "NOT NULL" if not self.allow_none else None,
        )))
        
        
    def get_type_from_annotations(self, owner):
        if (ann := getattr(owner, "__annotations__", None)) is not None:
            if (t := ann.get(self.field_name, None)) is not None:
                self.types = TE.extract(t)
                
                
    def _update_types(self):
        if type(None) in self.types or self.allow_none:
            self.allow_none = True
            if not type(None) in self.types:
                self.types = (type(None), *self.types)