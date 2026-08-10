from .base import BaseMixin
from ...tools import *



class QueryMixin(BaseMixin):
    def select(
        self, 
        table_name: TableName, 
        columns: list[ColumnName] | None = None, 
        where: WhereDict = None, 
        order_by: str | None = None,
        limit: int = None, 
        offset: int | None = None,
        distinct: bool = False) -> list[QueryDict]:
        
        cols = ", ".join(map(quote, columns)) if columns else "*"
        dist = "DISTINCT " if distinct else ""
        query = f"SELECT {dist}{cols} FROM {quote(table_name)}"
        params = ()
        
        if where:
            where_clause = " AND ".join([f"{quote(k)} = ?" for k in where.keys()])
            query += f" WHERE {where_clause}"
            params = tuple(where.values())
            
        if order_by:
            query += f" ORDER BY {order_by}"
            
        if limit is not None:
            query += f" LIMIT {limit}"
            if offset is not None:
                query += f" OFFSET {offset}"
                
        self.execute(query, params)
        return list(map(QueryDict, self.cursor.fetchall()))
        
        
    def select_all(self, table_name: TableName) -> list[QueryDict]:
        return self.select(table_name=table_name)
    
    
    def select_one(self, table_name: TableName, columns: list[ColumnName] | None = None, 
                   where: WhereDict = None, order_by: str | None = None) -> QueryDict | None:
        data = self.select(table_name, columns, where, order_by, limit=1)
        return data[0] if data else None
    
    
    def select_by_id(self, table_name: TableName, id: ID, columns: list[ColumnName] | None = None) -> QueryDict | None:
        return self.select_one(table_name=table_name, columns=columns, where={"id": id})
        
        
    def find_matches(self, table_name: TableName, columns: list[ColumnName], column_find: ColumnName, value, limit: int):
        cols = ", ".join(map(quote, columns)) if columns else "*"
        query = f"SELECT {cols} FROM {quote(table_name)} WHERE INSTR(LOWER({column_find}), LOWER(?)) = 1 LIMIT ?"
        self.execute(query, (value, limit))
        return list(map(QueryDict, self.cursor.fetchall()))