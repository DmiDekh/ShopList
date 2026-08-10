from typing import Any



type TableName = str
"""Ex: "items"; only lower names"""

type ColumnName = str
"""Ex: id"""

type ColumnType = str
"""Ex: INTEGER"""

type ColumnDef = str
"""Ex: "id" INTEGER PRIMARY KEY"""

type WhereDict = dict[str, Any]

type DataDict = dict[str, Any]

type ID = int