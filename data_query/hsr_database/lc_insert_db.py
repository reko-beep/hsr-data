import sqlite3 as sql
import json
import os
from data_query.lightcones_data import LightCone
from data_query.fsearch.db.leven_search import fsearch
import data_query.shared_data.shared_var as SharedVar
from dotenv import dotenv_values

key = dotenv_values(".env")


def db_connect(choice):
    if choice == "lc":
        return sql.connect(key["LIGHTCONE"])
    elif choice == "fsearch":
        return sql.connect(key["FSEARCH_DB_LOCATION"])
    else:
        return None


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
        lc_id INTEGER, 
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
        lc_id INTEGER,
        promotion INTEGER,
        cost TEXT,
        FOREIGN KEY(promotion) REFERENCES lc_level(promotion),
        FOREIGN KEY(lc_id) REFERENCES lightcones(lc_id)
        )
        """
    cursor.execute(Q_CREATE_LC_LEVEL)
    cursor.execute(Q_CREATE_LC_LEVEL_COST)


# {'promotion': 6, 'maxLevel': 80, 'cost': [], 'attackBase': 146.88, 'attackAdd': 2.16,
# 'hpBase': 391.68, 'hpAdd': 5.76, 'defenseBase': 122.4, 'defenseAdd': 1.8}


def insert_data_level_onlevel(conn):
    cursor = conn.cursor()
    lc_ids = cursor.execute("SELECT lc_id FROM lightcones")
    data_lc_level = []
    data_lc_level_cost = []
    for id in lc_ids:
        for index in SharedVar.level():
            level_data = LightCone(id[0]).level_data_onlevel(index)
            lc_id = id[0]
            promotion = level_data["promotion"]
            max_level = level_data["maxLevel"]
            cost = level_data["cost"]
            attack_base = level_data["attackBase"]
            attack_add = level_data["attackAdd"]
            hp_base = level_data["hpBase"]
            hp_add = level_data["hpAdd"]
            defense_base = level_data["defenseBase"]
            defense_add = level_data["defenseAdd"]
            data_lc_level.append(
                (
                    lc_id,
                    promotion,
                    max_level,
                    attack_base,
                    attack_add,
                    hp_base,
                    hp_add,
                    defense_base,
                    defense_add,
                )
            )
            data_lc_level_cost.append((lc_id, promotion, json.dumps(cost)))

    Q_INSERT_INTO_LC_LEVEL = "INSERT INTO lc_level VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)"
    Q_INSERT_INTO_LC_LEVEL_COST = "INSERT INTO lc_level_cost VALUES(?, ?, ?)"
    cursor.executemany(Q_INSERT_INTO_LC_LEVEL, data_lc_level)
    conn.commit()
    cursor.executemany(Q_INSERT_INTO_LC_LEVEL_COST, data_lc_level_cost)
    conn.commit()
    conn.close()

insert_data_level_onlevel(db_connect("lc"))
# create_table_level_onlevel(db_connect("lc"))