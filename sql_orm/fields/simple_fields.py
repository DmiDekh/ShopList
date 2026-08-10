from typing import Callable
from dataclasses import dataclass, field
from datetime import datetime

from .base import Field, SQLType



@dataclass
class StrField(Field[str]):
    types: type = field(default=str, init=False)
    converter: Callable = field(default=None, init=False)
    validate_value: Callable = field(default=None, init=False)
    serialize: Callable = field(default=None, init=False)
    deserialize: Callable = field(default=None, init=False)
    sql_type: SQLType = field(default=SQLType.TEXT, init=False)
    
    
        
@dataclass
class IntField(Field[int]):
    types: type = field(default=int, init=False)
    converter: Callable = field(default=None, init=False)
    validate_value: Callable = field(default=None, init=False)
    serialize: Callable = field(default=None, init=False)
    deserialize: Callable = field(default=None, init=False)
    sql_type: SQLType = field(default=SQLType.INTEGER, init=False)
   
        
        
@dataclass
class FloatField(Field[float]):
    types: type = field(default=float, init=False)
    converter: Callable = field(default=None, init=False)
    validate_value: Callable = field(default=None, init=False)
    serialize: Callable = field(default=None, init=False)
    deserialize: Callable = field(default=None, init=False)
    sql_type: SQLType = field(default=SQLType.REAL, init=False)
        


@dataclass
class BoolField(Field[bool]):
    types: type = field(default=bool, init=False)
    converter: Callable = field(default=None, init=False)
    validate_value: Callable = field(default=None, init=False)
    serialize: Callable = field(default=None, init=False)
    deserialize: Callable = field(default=None, init=False)
    sql_type: SQLType = field(default=SQLType.INTEGER, init=False)
    
    
    @staticmethod
    def field_serialize(value):
        return 1 if value else 0
    
    
    @staticmethod
    def field_deserialize(value):
        return True if value else False
        
        
        
@dataclass
class DatetimeField(Field[datetime]):
    types: type = field(default=datetime, init=False)
    converter: Callable = field(default=None, init=False)
    validate_value: Callable = field(default=None, init=False)
    serialize: Callable = field(default=None, init=False)
    deserialize: Callable = field(default=None, init=False)
    sql_type: SQLType = field(default=SQLType.TEXT, init=False)
    
    
    @staticmethod
    def field_serialize(value):
        return value.strftime("%d.%m.%Y, %H:%M:%S") if value is not None else None
    
    
    @staticmethod
    def field_deserialize(value):
        return datetime.strptime(value, "%d.%m.%Y, %H:%M:%S") if value is not None else None
