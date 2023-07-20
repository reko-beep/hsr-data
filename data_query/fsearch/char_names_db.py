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


def check_files_rawdata() -> list[str]:
    filenames: list[str] = [
        filename.replace(".json", "")
        for filename in os.listdir("raw_data/en/characters")
        if ".json" in filename
    ]
    return filenames


def insert_data_names(conn: sql.Connection) -> None:
    cursor: sql.Cursor = conn.cursor()
    filenames: list[str] = check_files_rawdata()
    data: list[tuple] = [(name, Character(name).name()) for name in filenames]
    cursor.executemany("INSERT OR IGNORE INTO char_names VALUES(?, ?)", data)
    conn.commit()
