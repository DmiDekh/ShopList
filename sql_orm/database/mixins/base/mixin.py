from typing import overload
import sqlite3 as sql
from pathlib import Path

from ....tools import *


class BaseMixin:
    path: Path
    connect: sql.Connection
    cursor: sql.Cursor
    _in_transaction: bool
    
    @overload
    def execute(self, command: str, params: tuple): ...
    
    
    def quote(self, table_name: str) -> TableName:
        return f'"{table_name.replace('"', '')}"'