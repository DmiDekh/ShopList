from pathlib import Path
import sqlite3 as sql

from .mixins import *


class Database(ExecutionMixin, SchemaMixin, CRUDMixin, QueryMixin, ModelManagerMixin):
    def __init__(self, path: Path):
        self.path = path
        
        self.connect = sql.connect(path)
        self.connect.create_function("LOWER", 1, lambda text: text.lower() if text else None)
        self.connect.row_factory = sql.Row
        self.cursor = self.connect.cursor()
        self._in_transaction = False
        
        
        