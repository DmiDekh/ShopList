from ...fields import *



class MetaclassModel(type):
    def __new__(mcls, name, bases, attrs):
        fields = {}
        for base in bases:
            fields.update(getattr(base, "_fields", {}))
        
        for attr_name, attr in attrs.items():
            if isinstance(attr, Field):
                fields[attr_name] = attr
        
        attrs["_fields"] = fields
        return super().__new__(mcls, name, bases, attrs)