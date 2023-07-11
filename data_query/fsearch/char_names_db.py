import sqlite3 as sql
import os
from data_query.character_data import Character
from dotenv import dotenv_values

key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["FSEARCH_DB_LOCATION"])


def create_table(conn) -> None:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS char_names(filename, name)")


def show_tables(conn) -> list[tuple]:
    cursor = conn.cursor()
    res = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return res.fetchall()


def show_table_content(conn) -> list[tuple]:
    cursor = conn.cursor()
    res = cursor.execute("PRAGMA table_info(char_names)")
    return res.fetchall()


def insert_data_names(conn) -> None:
    cursor = conn.cursor()
    filename = [
        filename.replace(".json", "")
        for filename in os.listdir("raw_data/en/characters")
        if ".json" in filename
    ]
    data = [(name, Character(name).name()) for name in filename]
    cursor.executemany("INSERT INTO char_names VALUES(?, ?)", data)
    conn.commit()
    conn.close()


def check_db() -> list[tuple]:
    new_con = sql.connect(key["FSEARCH_DB_LOCATION"])
    cursor = new_con.cursor()
    res = cursor.execute("SELECT * FROM char_names")
    return res.fetchall()


if __name__ == "__main__":
    # create_table(db_connect())
    # insert_data()
    # print(show_table_content())
    print(check_db())
    pass
