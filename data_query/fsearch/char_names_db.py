import sqlite3 as sql
import os
from pathlib import Path
from data_query.character_data import Character
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["FSEARCH_DB"])


def create_table(conn: sql.Connection) -> None:
    cursor: sql.Cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS char_names(filename, name)")


def show_tables(conn: sql.Connection) -> list[tuple]:
    cursor: sql.Cursor = conn.cursor()
    res: sql.Cursor = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    return res.fetchall()


def show_table_content(conn: sql.Connection) -> list[tuple]:
    cursor: sql.Cursor = conn.cursor()
    res: sql.Cursor = cursor.execute("PRAGMA table_info(char_names)")
    return res.fetchall()


def insert_data_names(conn: sql.Connection) -> None:
    cursor: sql.Cursor = conn.cursor()
    filenames: list[str] = [
        filename.replace(".json", "")
        for filename in os.listdir("raw_data/en/characters")
        if ".json" in filename
    ]
    data: list[tuple] = [(name, Character(name).name()) for name in filenames]
    cursor.executemany("INSERT INTO char_names VALUES(?, ?)", data)
    conn.commit()
    conn.close()


def check_db() -> list[tuple] | None:
    if key["FSEARCH_DB"] is not None:
        new_con: sql.Connection = sql.connect(key["FSEARCH_DB"])
        cursor: sql.Cursor = new_con.cursor()
        res: sql.Cursor = cursor.execute("SELECT * FROM char_names")
        return res.fetchall()
    else:
        return None


if __name__ == "__main__":
    # create_table(db_connect())
    # insert_data()
    # print(show_table_content())
    # print(check_db())
    pass
