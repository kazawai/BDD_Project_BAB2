import sqlite3 as sql
import os
from Class.Operator import *

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
        tables = [table2, table1]

    if tables_struct is None:
        table_struct1 = """ Name TEXT PRIMARY KEY,
                        Country TEXT,
                        Inhabitants INTEGER,
                        FOREIGN KEY(Country) REFERENCES Country(Name)
                        """
        table_struct2 = """ Name TEXT PRIMARY KEY,
                        Capital TEXT,
                        Inhabitants INTEGER,
                        Continent TEXT,
                        Currency TEXT
                        """
        tables_struct = [table_struct2, table_struct1]

    # We will assume that the table_struct is nicely formatted if given
    for i in range(len(tables)):
        cur.execute(f"CREATE TABLE {tables[i]} ({tables_struct[i]});")

    cur.execute(f"INSERT INTO {table2} VALUES (\"USA\", \"Washington\", \"30000000\", \"North America\", \"USD\");")

    con.commit()
    con.close()


def run_query(name: str, query: Operator):
    con = sql.connect(f"{name}.db")
    cur = con.cursor()

    print(f"\n\n{query.query}\n")

    cur.execute(query.query)

    print(query.format(cur.fetchall()))

    con.close()


if __name__ == "__main__":
    pass

