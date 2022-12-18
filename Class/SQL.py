from Class.Errors import TableNameException

class Attribute:

    def __init__(self, a_name: str):
        self.a_name = a_name

    def __str__(self):
        return str(self.a_name)

    def __eq__(self, other: "Attribute"):
        if isinstance(other, Attribute):
            return self.a_name == other.get_name()
        return False

    def get_name(self):
        return self.a_name

    def is_type(self, o_type: str):
        return o_type == self.a_name

    # String as parameter type to avoid error (called forward reference :
    # https://peps.python.org/pep-0484/#forward-references)
    def can_compare(self, o_attr: "Attribute"):
        if self.a_name != o_attr.get_name():
            return False
        return True


class Constant:

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return str(self.name)

    def __eq__(self, other: "Constant"):
        if isinstance(other, Constant):
            return self.name == other.name
        return False


import sqlite3


class Table:

    def __init__(self, db: str, name: str, attr_list=None, row_list=None, past_name=None):
        self.db = Database(db)
        self.name = name
        self.attr = attr_list if attr_list is not None else self.get_attr()
        self.row = row_list if row_list is not None else self.get_rows()
        self.past_name = past_name

    def get_attr(self):
        attr = self.db.run(f"PRAGMA table_info([{self.name}])")
        return [element[1] for element in attr]

    def get_rows(self):
        return self.db.run(f"SELECT DISTINCT * FROM [{self.name}]")

    def __str__(self):
        return self.name


class Database:

    def __init__(self, name: str):
        self.name = name
        self.connection = sqlite3.connect(f"{name}.db")
        self.cur = self.connection.cursor()
        self.tables = self.get_tables()

    def get_tables(self):
        query = "SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"
        return [table[0] for table in self.run(query)]

    def run(self, query: str):
        try:
            return self.cur.execute(query).fetchall()
        except sqlite3.OperationalError as e:
            raise TableNameException(f"{self.name}.db : {e}")

    def close(self):
        return self.connection.close()
