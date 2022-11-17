import sqlite3 as sql

global cur

if __name__ == "__main__":
    con = sql.connect("database.db")
    cur = con.cursor()

