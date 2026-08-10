import typing
import types



class TypeExtractor:
    def __init__(self):
        self.methods = {
            typing._UnionGenericAlias: self._get_args,
            types.UnionType: self._get_args,
            typing.TypeAliasType: self._extract_TypeAliasType,
        }
        
        
    def extract(self, _type: type | tuple[type, ...]) -> tuple[type, ...]:
        type_set = set() 
        self._extract(_type, type_set)
        return tuple(type_set)
    
    
    def _extract(self, _type: type, type_set: set):
        if isinstance(_type, (tuple, list)):
            for t in _type:
                self._extract(t, type_set)
                
        elif (method := self.methods.get(type(_type), None)) is not None:
            self._extract(method(_type), type_set)
        
        else:
            if _type is None:
                _type = type(None)
            type_set.add(_type)
            
            
    def _get_args(self, obj):
        return typing.get_args(obj)
    
    
    def _get_origin(self, obj):
        return typing.get_origin(obj)
    
    
    def _extract_TypeAliasType(self, obj: typing.TypeAliasType):
        return obj.__value__