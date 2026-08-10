from typing import Self
from functools import wraps

from .base import BaseMixin
from ...tools import *
from ...fields import Field


def require_db(func):
    @wraps(func)
    def wrapper(self: "BaseMixin", *args, **kwargs):
        if self._db is not None:
            return func(self, *args, **kwargs)
        raise Exception(f"There is no connection to the database to execute the function {func.__name__}")
    return wrapper



class DatabaseMethodsMixin(BaseMixin):
    @classmethod
    @require_db
    def create(cls, **data) -> Self:
        ins = cls(**data)
        ins._id = cls._db.insert(cls._table_name, ins.to_dict(serialize=True), return_id=True)
        cls._cache[ins.id] = ins
        return ins
    
    
    @classmethod
    @require_db
    def get(cls, **where) -> Self | None:
        where = {f_n: cls._fields[f_n].serialize(value) for f_n, value in where.items()}
        if (data := cls._db.select_one(table_name=cls._table_name, where=where)) is not None:
            if (model := cls._cache.get(data.get("id"))) is not None:
                return model
            return cls.from_dict(data)
        return None
    
    
    @classmethod
    @require_db
    def get_by_id(cls, id: ID):
        if (model := cls._cache.get(id)) is not None:
            return model
        return cls.from_dict(data) if (data := cls._db.select_by_id(cls._table_name, id)) else None
    
    
    @classmethod
    @require_db
    def get_all(cls):
        return [cls.from_dict(data) for data in cls._db.select_all(cls._table_name)]
    
    
    @classmethod
    @require_db
    def get_or_create(cls, **where) -> Self:
        if (model := cls.get(**where)) is not None:
            return model
        return cls.create(**where)
    
    
    @require_db
    def save(self):
        self._db.update_by_id(self._table_name, self.to_dict(serialize=True), self.id)
        
        
    @require_db
    def delete(self):
        self._db.delete_by_id(self._table_name, self.id)
        self._cache.pop(self.id, None)
    
    
    def _update_by_field(self, field: Field):
        if self.auto_save and self._db is not None:
            self._db.update_by_id(
                self._table_name, 
                {field.field_name: field.serialize(getattr(self, field.field_name))}, 
                self.id)