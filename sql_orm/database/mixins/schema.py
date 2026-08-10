from ...tools import *
from .base import BaseMixin



class SchemaMixin(BaseMixin):
    def create_table(self, table_name: TableName, columns_def: list[ColumnDef]):
        fields = ", ".join(columns_def)
        self.execute(f"CREATE TABLE IF NOT EXISTS {quote(table_name)} ({fields})")
        
        
    def rename_table(self, old_table_name: TableName, new_table_name: TableName):
        self.execute(f"ALTER TABLE {quote(old_table_name)} RENAME TO {quote(new_table_name)}")
        
        
    def clear_table(self, table_name: TableName, reset_autoincrement: bool = True):
        self.execute(f"DELETE FROM {quote(table_name)}")
        if reset_autoincrement:
            self.execute("DELETE FROM sqlite_sequence WHERE name = ?", (table_name,))
        
        
    def delete_table(self, table_name: TableName):
        self.execute(f"DROP TABLE IF EXISTS {quote(table_name)}")
        
    
    # ============= Column
    def add_column(self, table_name: TableName, column_def: ColumnDef):
        self.execute(f"ALTER TABLE {quote(table_name)} ADD COLUMN {column_def}")
            
            
    def rename_column(self, table_name: TableName, old_column_name: ColumnName, new_column_name: ColumnName):
        self.execute(f"ALTER TABLE {quote(table_name)} RENAME COLUMN {quote(old_column_name)} TO {quote(new_column_name)}")
            
            
    def delete_column(self, table_name: TableName, column_name: ColumnName):
        self.execute(f"ALTER TABLE {quote(table_name)} DROP COLUMN {quote(column_name)}")