import sqlite3
import os
from data_query.books_data import Books
from pathlib import Path
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")

conn = sqlite3.connect(key["FSEARCH_DB"])


def create_table_books(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS books_names("
        "id INTEGER PRIMARY KEY,"
        "name TEXT"
        ")"
    )


def insert_data_books(conn: sqlite3.Connection):
    cursor = conn.cursor()
    filenames: list[int] = [
        int(filename.replace(".json", ""))
        for filename in os.listdir("raw_data/en/books")
        if ".json" in filename
    ]
    data_books = []
    for id in filenames:
        books = Books(id)
        name: str = books.name()
        books_id: int = books.book_id()
        data_books.append({"name": name, "id": books_id})

    Q_INSERT_INTO_BOOKS_FSEARCH = """INSERT INTO books_names(
    id,
    name
    ) VALUES(
    :id,
    :name
    )
    """
    cursor.executemany(Q_INSERT_INTO_BOOKS_FSEARCH, data_books)
    conn.commit()
    conn.close()
