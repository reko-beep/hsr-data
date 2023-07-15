import sqlite3 as sql
import os
from pathlib import Path
from data_query.relics_data import Relic
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["FSEARCH_DB"])


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS relics_name(id, name)")


def insert_data(conn):
    cursor = conn.cursor()
    filename = [
        int(filename.replace(".json", ""))
        for filename in os.listdir("raw_data/en/relics")
        if ".json" in filename
    ]
    data = [(Relic(num).id(), Relic(num).name()) for num in filename]
    q = "INSERT INTO relics_name VALUES (?, ?)"
    cursor.executemany(q, data)
    conn.commit()
    conn.close()
