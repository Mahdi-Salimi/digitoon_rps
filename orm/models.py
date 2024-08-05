class Field:
    def __init__(self, column_type: str):
        self.column_type = column_type

class IntegerField(Field):
    def __init__(self):
        super().__init__("INTEGER")

class StringField(Field):
    def __init__(self):
        super().__init__("TEXT")
