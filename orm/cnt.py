import sqlite3
import os
from typing import List, Optional

'''
This class will handle connections to the database
'''
class Connections:
    def __init__(self, db_name='orm.db'):
        self.connection = sqlite3.connect(db_name)
    
    def execute(self, query: str, params: Optional[tuple] = ()) -> sqlite3.Cursor:
        with self.connection:
            return self.connection.execute(query, params)

    def fetchall(self, query: str, params: tuple = ()) -> List[tuple]:
        with self.connection:
            cursor = self.connection.execute(query, params)
            return cursor.fetchall()

    def fetchone(self, query: str, params: tuple = ()) -> tuple:
        with self.connection:
            cursor = self.connection.execute(query, params)
            return cursor.fetchone()
    
    def create_table(self, create_table_sql: str) -> None:
        self.execute(create_table_sql)
    
    def get_table_columns(self, table_name: str) -> List[str]:
        cursor = self.execute(f"PRAGMA table_info({table_name})")
        return [row[1] for row in cursor.fetchall()]
    
    
db = Connections()