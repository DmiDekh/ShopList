from typing import Self, overload

from ...database import Database
from ...tools import *



class BaseMixin:
    _cache: dict[int, Self]
    
    id: int | None
    auto_save: bool
    
    _id: int | None
    _db: Database
    _table_name: TableName
    
    @overload
    def to_dict(self, serialize: bool = False, with_id: bool = False) -> DataDict: ...
    
    @overload
    @classmethod
    def from_dict(cls, data: DataDict) -> Self: ...
    