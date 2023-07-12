import sqlite3 as sql
import os
from data_query.lightcones_data import LightCone
from data_query.fsearch.db.leven_search import fsearch
from dotenv import dotenv_values

key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["LIGHTCONE"])


def db_connect_fsearch():
    return sql.connect(key["FSEARCH_DB_LOCATION"])


def fuzzysearch(entry):
    cursor = db_connect_fsearch().cursor()
    names = cursor.execute("SELECT name FROM lc_names")
    names_list = [name[0] for name in names]
    fsearch_name = fsearch(entry, names_list)
    return fsearch_name


def create_table_primary(conn):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS lightcones("
        "lc_id INTEGER PRIMARY KEY, "
        "name TEXT, "
        "rarity INTEGER)"
    )


def insert_data_primary(conn):
    cursor = conn.cursor()
    filenames = os.listdir("raw_data/en/lightcones")
    lcs_id = [
        int(lc_id.replace(".json", "")) for lc_id in filenames if ".json" in lc_id
    ]
    data = [
        (LightCone(id).lc_id(), LightCone(id).name(), LightCone(id).rarity())
        for id in lcs_id
    ]
    q = "INSERT INTO lightcones VALUES (?, ?, ?)"
    cursor.executemany(q, data)
    conn.commit()
    conn.close()


def create_table_level_onlevel(conn):
    cursor = conn.cursor()
    Q_CREATE_LC_LEVEL = """CREATE TABLE IF NOT EXISTS lc_level(
        lc_id INTEGER PRIMARY KEY, 
        promotion INTEGER, 
        max_level INTEGER, 
        attack_base FLOAT, 
        attack_add FLOAT, 
        hp_base FLOAT, 
        hp_add FLOAT, 
        defense_base FLOAT, 
        defense_add FLOAT,
        FOREIGN KEY(lc_id) REFERENCES lightcones(lc_id)
        )
        """

    Q_CREATE_LC_LEVEL_COST = """CREATE TABLE IF NOT EXISTS lc_level_cost(
        lc_id INTEGER PRIMARY KEY,
        promotion INTEGER,
        cost TEXT,
        FOREIGN KEY(promotion) REFERENCES lc_level(promotion),
        FOREIGN KEY(lc_id) REFERENCES lightcones(lc_id)
        )
        """
    cursor.execute(Q_CREATE_LC_LEVEL_COST)


create_table_level_onlevel(db_connect())
