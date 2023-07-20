import sqlite3
import json
import os
from pathlib import Path
from typing import Any
from data_query.lightcones_data import LightCone
from data_query.fsearch.db.leven_search import fsearch
import data_query.shared_data.shared_var as SharedVar
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")


def db_connect(choice: str | None = None) -> sqlite3.Connection | None:
    if choice is None or None in key.values():
        return
    if choice == "lc":
        return sqlite3.connect(key["LIGHTCONE"])
    elif choice == "fsearch":
        return sqlite3.connect(key["FSEARCH_DB_LOCATION"])
    elif choice == "test":
        return sqlite3.connect(key["TESTDUMP_HSR_DB"])
    else:
        return


def create_table_primary(conn: sqlite3.Connection) -> None:
    cursor: sqlite3.Cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS lightcones("
        "lc_id INTEGER PRIMARY KEY, "
        "name TEXT, "
        "rarity INTEGER"
        ")"
        "STRICT"
    )


def insert_data_primary(conn: sqlite3.Connection) -> None:
    cursor: sqlite3.Cursor = conn.cursor()
    filenames: list = os.listdir("raw_data/en/lightcones")
    lcs_id: list[int] = [
        int(lc_id.replace(".json", "")) for lc_id in filenames if ".json" in lc_id
    ]
    data: list[tuple[int, str, int]] = [
        (LightCone(id).lc_id(), LightCone(id).name(), LightCone(id).rarity())
        for id in lcs_id
    ]
    q: str = "INSERT OR IGNORE INTO lightcones VALUES (?, ?, ?)"
    cursor.executemany(q, data)
    conn.commit()
    conn.close()


def create_table_level_onlevel(conn: sqlite3.Connection) -> None:
    cursor: sqlite3.Cursor = conn.cursor()
    Q_CREATE_LC_LEVEL = """CREATE TABLE IF NOT EXISTS lc_level(
    p_key INTEGER PRIMARY KEY,
    lc_id INTEGER, 
    promotion INTEGER, 
    max_level INTEGER, 
    attack_base REAL, 
    attack_add REAL, 
    hp_base REAL, 
    hp_add REAL, 
    defense_base REAL, 
    defense_add REAL,
    FOREIGN KEY(lc_id) REFERENCES lightcones(lc_id)
    )
    STRICT
    """

    Q_CREATE_LC_LEVEL_COST = """CREATE TABLE IF NOT EXISTS lc_level_cost(
    p_key INTEGER PRIMARY KEY,
    lc_id INTEGER,
    promotion INTEGER,
    cost TEXT,
    FOREIGN KEY(lc_id) REFERENCES lightcones(lc_id)
    )
    STRICT
    """
    cursor.execute(Q_CREATE_LC_LEVEL)
    cursor.execute(Q_CREATE_LC_LEVEL_COST)


# {'promotion': 6, 'maxLevel': 80, 'cost': [], 'attackBase': 146.88, 'attackAdd': 2.16,
# 'hpBase': 391.68, 'hpAdd': 5.76, 'defenseBase': 122.4, 'defenseAdd': 1.8}


def insert_data_level_onlevel(conn: sqlite3.Connection) -> None:
    cursor: sqlite3.Cursor = conn.cursor()
    lc_ids: sqlite3.Cursor = cursor.execute("SELECT lc_id FROM lightcones")
    data_lc_level = []
    data_lc_level_cost = []
    for id in lc_ids:
        for index in SharedVar.level():
            level_data: dict | None = LightCone(id[0]).level_data_onlevel(index)
            lc_id: int = id[0]
            if level_data is None:
                return
            promotion: int = level_data["promotion"]
            max_level: int = level_data["maxLevel"]
            p_key_onlevel: int = int(str(max_level) + str(lc_id))
            p_key_cost: int = int(str(promotion) + str(lc_id))
            cost: list = level_data["cost"]
            attack_base: float = level_data["attackBase"]
            attack_add: float = level_data["attackAdd"]
            hp_base: float = level_data["hpBase"]
            hp_add: float = level_data["hpAdd"]
            defense_base: float = level_data["defenseBase"]
            defense_add: float = level_data["defenseAdd"]
            data_lc_level.append(
                {
                    "p_key": p_key_onlevel,
                    "lc_id": lc_id,
                    "promotion": promotion,
                    "max_level": max_level,
                    "attack_base": attack_base,
                    "attack_add": attack_add,
                    "hp_base": hp_base,
                    "hp_add": hp_add,
                    "defense_base": defense_base,
                    "defense_add": defense_add,
                }
            )
            data_lc_level_cost.append(
                {
                    "p_key": p_key_cost,
                    "lc_id": lc_id,
                    "promotion": promotion,
                    "cost": json.dumps(cost),
                }
            )
    Q_INSERT_INTO_LC_LEVEL = """INSERT INTO lc_level(
    p_key,
    lc_id,
    promotion,
    max_level,
    attack_base,
    attack_add,
    hp_base,
    hp_add,
    defense_base,
    defense_add
    ) VALUES(
    :p_key,
    :lc_id,
    :promotion,
    :max_level,
    :attack_base,
    :attack_add,
    :hp_base,
    :hp_add,
    :defense_base,
    :defense_add
    )
    """

    Q_INSERT_INTO_LC_LEVEL_COST = """INSERT OR IGNORE INTO lc_level_cost(
    p_key,
    lc_id,
    promotion,
    cost
    ) VALUES(
    :p_key,
    :lc_id,
    :promotion,
    :cost
    )
    """

    cursor.executemany(
        Q_INSERT_INTO_LC_LEVEL,
        data_lc_level,
    )
    conn.commit()
    cursor.executemany(
        Q_INSERT_INTO_LC_LEVEL_COST,
        data_lc_level_cost,
    )
    conn.commit()
    conn.close()


def create_table_skilldeschash(conn: sqlite3.Connection):
    cursor: sqlite3.Cursor = conn.cursor()
    Q_CREATE_TABLE_SKILLDESCHASH = """CREATE TABLE IF NOT EXISTS lc_skill_desc(
    p_key INTEGER PRIMARY KEY,
    lc_id INTEGER,
    level INTEGER,
    skill_deschash TEXT,
    FOREIGN KEY(lc_id) REFERENCES lightcones(lc_id)
    )
    STRICT
    """
    cursor.execute(Q_CREATE_TABLE_SKILLDESCHASH)


def insert_data_skill_deschash(conn: sqlite3.Connection) -> None:
    cursor: sqlite3.Cursor = conn.cursor()
    lc_ids: sqlite3.Cursor = cursor.execute("SELECT lc_id FROM lightcones")
    data_skill_deschash = []
    for id in lc_ids:
        for index in range(5):
            lc_id: int = id[0]
            level: int = index + 1
            p_key_skilldesc: int = int(str(level) + str(lc_id))
            description: str | None = LightCone(id[0]).skill_descHash(index + 1)

            data_skill_deschash.append(
                {
                    "p_key": p_key_skilldesc,
                    "lc_id": lc_id,
                    "level": level,
                    "skill_descHash": description,
                }
            )
    Q_INSERT_INTO_LC_SKILL_DESC = """INSERT OR IGNORE INTO lc_skill_desc(
    p_key,
    lc_id,
    level,
    skill_deschash
    ) VALUES(
    :p_key,
    :lc_id,
    :level,
    :skill_descHash
    )
    """
    cursor.executemany(Q_INSERT_INTO_LC_SKILL_DESC, data_skill_deschash)
    conn.commit()
