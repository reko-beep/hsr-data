import sqlite3 as sql
import os
from pathlib import Path
from data_query.lightcones_data import LightCone
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["FSEARCH_DB"])


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS lc_names("
        "id INTEGER PRIMARY KEY, "
        "name TEXT"
        ")"
        "STRICT"
    )


def insert_data_lightcones(conn):
    cursor = conn.cursor()
    filenames = os.listdir("raw_data/en/lightcones")
    lcs_id = [
        int(lc_id.replace(".json", "")) for lc_id in filenames if ".json" in lc_id
    ]
    data = [(id, LightCone(id).name()) for id in lcs_id]
    q = "INSERT OR IGNORE INTO lc_names VALUES (?, ?)"
    cursor.executemany(q, data)
    conn.commit()


def check_db():
    new_con = sql.connect(key["FSEARCH_DB"])
    cursor = new_con.cursor()
    res = cursor.execute("SELECT * FROM lc_names")
    print(res.fetchall())
