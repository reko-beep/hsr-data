import sqlite3
from dotenv import dotenv_values
from data_query.relics_data import Relic

key = dotenv_values(".env")


def db_connect(choice: str | None = None):
    if choice is None:
        return
    if choice == "relics":
        return sqlite3.connect("db/relics.db")


def create_table_primary(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relics("
        "relic_id INTEGER PRIMARY KEY,"
        "name TEXT,"
        "rarity INTEGER"
        ")"
    )
