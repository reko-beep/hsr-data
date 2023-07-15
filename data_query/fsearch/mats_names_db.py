import sqlite3 as sql
import os
from pathlib import Path
from data_query.materials_data import Materials
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["FSEARCH_DB"])


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS mats_names(id, name, rarity)")


def insert_data(conn):
    cursor = conn.cursor()
    filenames = os.listdir("raw_data/en/materials")
    mats_id = [
        int(mat_id.replace(".json", "")) for mat_id in filenames if ".json" in mat_id
    ]
    data = [
        (Materials(id).id(), Materials(id).name(), Materials(id).rarity())
        for id in mats_id
    ]
    ordered_data = sorted(data, key=lambda x: x[0])
    q = "INSERT INTO mats_names VALUES(?, ? ,?)"
    cursor.executemany(q, data)
    conn.commit()
    conn.close()


def check_db():
    conn = db_connect()
    cursor = conn.cursor()
    res = cursor.execute("SELECT id, name, rarity FROM mats_names ORDER BY rarity")
    print(res.fetchall())


if __name__ == "__main__":
    check_db()
