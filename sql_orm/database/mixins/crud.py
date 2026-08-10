from .base import BaseMixin
from ...tools import *



class CRUDMixin(BaseMixin):
    def insert(self, table_name: TableName, data: DataDict, return_id: bool = False) -> ID | None:
        if data:
            fields = ", ".join(map(quote, data.keys()))
            num_values = ", ".join("?" * len(data))
            self.execute(f"INSERT INTO {quote(table_name)} ({fields}) VALUES ({num_values})", tuple(data.values()))
            if return_id:
                return self.cursor.lastrowid
            
            
    # UPDATE
    def update_by(self, table_name: TableName, data: DataDict, where: WhereDict):
        if data and where:
            set_clause = ", ".join([f"{quote(k)} = ?" for k in data.keys()])
            where_clause = " AND ".join([f"{quote(k)} = ?" for k in where.keys()])
            command = f"UPDATE {quote(table_name)} SET {set_clause} WHERE {where_clause}"
            self.execute(command, (*data.values(), *where.values()))
        
        
    def update_by_id(self, table_name: TableName, data: DataDict, id: ID):
        self.update_by(table_name, data, {"id": id})
        
    
    # DELETE
    def delete_by(self, table_name: TableName, where: WhereDict):
        if where:
            where_clause = " AND ".join([f"{quote(k)} = ?" for k in where.keys()])
            self.execute(f"DELETE FROM {quote(table_name)} WHERE {where_clause}", tuple(where.values()))
            
            
    def delete_by_id(self, table_name: TableName, id: ID):
        self.delete_by(table_name, where={"id": id})
            