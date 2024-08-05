from typing import Dict, List, Any, Tuple, Type
from .cnt import db


class Field:
    def __init__(self, column_type: str):
        self.column_type = column_type

class IntegerField(Field):
    def __init__(self):
        super().__init__("INTEGER")

class StringField(Field):
    def __init__(self):
        super().__init__("TEXT")
        


class ModelMeta(type):
    def __new__(cls: Type['ModelMeta'], name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> 'ModelMeta':
        if name == 'Model':
            return super().__new__(cls, name, bases, attrs)
        columns = {k: v for k, v in attrs.items() if isinstance(v, Field)}
        for column in columns.keys():
            attrs.pop(column)
        attrs['_columns'] = columns
        new_class = super().__new__(cls, name, bases, attrs)
        return new_class
   
    def __init__(cls: Type['Model'], name: str, bases: Tuple[type], attrs: Dict[str, Any]) -> None:
            super().__init__(name, bases, attrs)
            
class Model(metaclass=ModelMeta):
    _columns: Dict[str, Field]

    @classmethod
    def create_table(cls) -> None:
        columns = []
        for name, field in cls._columns.items():
            columns.append(f"{name} {field.column_type}")
        columns_def = ", ".join(columns)
        sql = f"CREATE TABLE IF NOT EXISTS {cls.__name__.lower()} (id INTEGER PRIMARY KEY, {columns_def})"
        db.create_table(sql)
        
    @classmethod
    def migrate(cls) -> None:
        table_name = cls.__name__.lower()
        existing_columns = db.get_table_columns(table_name)
        new_columns = cls._columns.keys()
        columns_to_add = set(new_columns) - set(existing_columns)

        for column in columns_to_add:
            field = cls._columns[column]
            sql = f"ALTER TABLE {table_name} ADD COLUMN {column} {field.column_type}"
            db.execute(sql)
        
        
    def save(self) -> None:
        columns = ', '.join(self._columns.keys())
        placeholders = ', '.join(['?' for _ in self._columns])
        values = [getattr(self, col) for col in self._columns.keys()]
        if self.id != None:
            values.append(self.id)
            db.execute(
                f"UPDATE {self.__class__.__name__.lower()} SET {', '.join(f'{col}=?' for col in self._columns)} WHERE id=?", 
                tuple(values)
            )
        else:
            db.execute(
                f"INSERT INTO {self.__class__.__name__.lower()} ({columns}) VALUES ({placeholders})", 
                tuple(values)
            )
            self.id = db.fetchone("SELECT last_insert_rowid()")[0]

    @classmethod
    def get(cls, **kwargs) -> 'Model':
        conditions = ' AND '.join([f"{k}=?" for k in kwargs.keys()])
        values = tuple(kwargs.values())
        row = db.fetchone(f"SELECT * FROM {cls.__name__.lower()} WHERE {conditions}", values)
        if row:
            return cls(**dict(zip(['id'] + list(cls._columns.keys()), row)))
        return None

    @classmethod
    def all(cls) -> List['Model']:
        rows = db.fetchall(f"SELECT * FROM {cls.__name__.lower()}")
        return [cls(**dict(zip(['id'] + list(cls._columns.keys()), row))) for row in rows]


