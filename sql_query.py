import sqlite3 as sql
import os

global cur


class AlreadyExistingError(Exception):

    def __init__(self, s: str = ""):
        super().__init__(s)


def create_db(name: str, tables: list = None, tables_struct: list = None):
    if os.path.exists(f"{name}.db"):
        raise AlreadyExistingError(f"The database \'{name}\' already exists")

    assert len(tables) == len(tables_struct) if tables is not None and tables_struct is not None else True
    assert tables == tables_struct if tables is None or tables_struct is None else True

    con = sql.connect(f"{name}.db")
    cur = con.cursor()

    if tables is None:
        table1 = "Cities"
        table2 = "Country"
        tables = [table1, table2]

    if tables_struct is None:
        table_struct1 = """ Name TEXT PRIMARY KEY
                        Country TEXT FOREIGN KEY REFERENCE Country
                        Inhabitants INTEGER
                        """
        table_struct2 = """ Name TEXT PRIMARY KEY
                        Capital TEXT
                        Inhabitants INTEGER
                        Continent TEXT
                        Currency TEXT
                        """
        tables_struct = [table_struct1, table_struct2]

    # We will assume that the table_struct is nicely formatted if given
    for i in range(len(tables)):
        cur.execute(f"CREATE TABLE {tables[i]} ({tables_struct[i]});")

    con.commit()
    con.close()


if __name__ == "__main__":
    pass

