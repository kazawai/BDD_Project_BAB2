import sqlite3
import sqlite3 as sql
import os
import uuid
from Class.Operator import *
from Class.SQL import *
from Class.Errors import *


def create_db(name: str, tables: list = None, tables_struct: list = None, test: bool = False):
    if os.path.exists(f"{name}.db") and not test:
        c = input(f"The database {name}.db already exists, would you like to reset it to the predefined values ? [y/n] : ")
        con = sql.connect(f"{name}.db")
        cur = con.cursor()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
        reply = cur.fetchall()

        if c == "y":
            table_names = map(lambda tup: tup[0], reply)
            for n in table_names:
                cur.execute(f"DROP TABLE {n}")
            con.commit()
            con.close()

        if c == "n":
            if any(['CC' not in [table[0] for table in reply], 'Cities' not in [table[0] for table in reply]]):
                raise WrongDatabaseException(f"{name}.db should at least contain tables 'CC' and 'Cities' but doesn't.\nDatabase's tables{[table[0] for table in reply]}")
            return

    assert len(tables) == len(tables_struct) if tables is not None and tables_struct is not None else True
    assert tables == tables_struct if tables is None or tables_struct is None else True

    con = sql.connect(f"{name}.db")
    cur = con.cursor()

    if tables is None:
        table1 = "Cities"
        table2 = "Country"
        table3 = "Country2"
        table4 = "CC"
        tables = [table2, table1, table3, table4]

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
        table_struct3 = """ Name TEXT PRIMARY KEY,
                                Capital TEXT,
                                Inhabitants INTEGER,
                                Continent TEXT,
                                Currency TEXT
                                """
        table_struct4 = """ Name TEXT PRIMARY KEY,
                                        Capital TEXT,
                                        Inhabitants INTEGER,
                                        Continent TEXT,
                                        Currency TEXT
                                        """
        tables_struct = [table_struct2, table_struct1, table_struct3, table_struct4]

    # We will assume that the table_struct is nicely formatted if given
    for i in range(len(tables)):
        cur.execute(f"CREATE TABLE {tables[i]} ({tables_struct[i]});")

    cur.execute(f"INSERT INTO {table1} VALUES (\"Brussels\", \"Belgium\", \"1\");")
    cur.execute(f"INSERT INTO {table1} VALUES (\"New-York\", \"USA\", \"5\");")
    cur.execute(f"INSERT INTO {table2} VALUES (\"USA\", \"Washington\", \"30000000\", \"North America\", \"USD\");")
    cur.execute(f"INSERT INTO {table2} VALUES (\"France\", \"Paris\", \"9\", \"Europe\", \"EUR\");")
    cur.execute(f"INSERT INTO {table3} VALUES (\"USA\", \"Washington\", \"30000000\", \"North America\", \"USD\");")
    cur.execute(f"INSERT INTO {table2} VALUES (\"Belgium\", \"Brussels\", \"1\", \"Europe\", \"EUR\");")
    cur.execute(f"INSERT INTO {table3} VALUES (\"France\", \"Paris\", \"-91\", \"Europe\", \"EUR\");")
    cur.execute(f"INSERT INTO {table3} VALUES (\"DbLand\", \"Rablgebra\", \"35\", \"Heaven\", \"DBC\");")

    con.commit()


def commit_query(query: "Operator"):
    con = sql.connect(f"{query.db.name}.db")
    try:
        cur = con.cursor()
        cur.execute(query.query)
        print(f"executed {query.printable_query}")
        con.commit()

        cur.execute(f"SELECT * FROM {query.table.name};")

        fetch = cur.fetchall()
        con.close()
        return Table(query.db.name, query.table.name, query.table.attr, fetch, query.table)
    except sqlite3.Error as e:
        print(f"Error while commit : {e}")
    finally:
        con.close()


query_list = []
def commit_queries():
    for queries in query_list:
        con = sql.connect(f"{queries[0].name}.db")
        try:
            cur = con.cursor()

            cur.execute(queries[1].commit_query)
            print(f"executed {queries[1].commit_query}")
            con.commit()
        except sqlite3.Error as e:
            print(f"Error : {e}")
        finally:
            con.close()


temp_tables = []


def delete_tables(db: str):
    for table in temp_tables:
        con = sql.connect(f"{db}.db")
        try:
            cur = con.cursor()

            cur.execute(f"DROP TABLE [{table}]")
            temp_tables.remove(table)
        except sqlite3.Error as e:
            print(f"Error : {e}")
        finally:
            con.close()


def create_table(db: Database, query: "Operator", table_id):
    con = sql.connect(f"{db.name}.db")
    try:
        cur = con.execute(f"CREATE TABLE [{table_id}] AS {query.query}")
        con.commit()
        cur = con.execute(f"PRAGMA table_info([{table_id}])")
        desc = cur.fetchall()
        temp_tables.append(table_id)
        return desc
    except sqlite3.Error as e:
        print(f"Error in create : {e}")
    finally:
        con.close()


def run_query(db: Database, query: "Operator") -> Table:
    con = sql.connect(f"{db.name}.db")
    try:
        cur = con.cursor()

        print(f"\n\nTranslated query : {query.printable_query if query.printable_query != '' else query.query}\n")

        cur.execute(query.query)

        query_list.append((db, query))

        table_id = uuid.uuid4()

        fetch = cur.fetchall()
        con.close()
        desc = create_table(db, query, str(table_id))
        return Table(db.name, str(table_id), [d[1] for d in desc], fetch, query.table)
    except sqlite3.Error as e:
        print(f"Error in run : {e}")
    finally:
        con.close()


if __name__ == "__main__":
    pass

