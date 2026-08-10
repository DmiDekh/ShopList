from enum import Enum



class SQLType(Enum):
    INTEGER = int
    REAL = float
    TEXT = str
    BLOB = bytes
    
    


class Unset:
    _instance = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    
    def __str__(self): 
        return "<UNSET>"