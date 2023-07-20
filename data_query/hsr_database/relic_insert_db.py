import sqlite3
import os
import json
from pathlib import Path
from dotenv import dotenv_values
from data_query.relics_data import Relic

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")


def db_connect(choice: str | None = None):
    if choice is None:
        return
    if choice == "relic":
        return sqlite3.connect(key["RELIC"])
    elif choice == "fsearch":
        return sqlite3.connect(key["FSEARCH_DB"])


def create_table_primary(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relics("
        "relic_id INTEGER PRIMARY KEY,"
        "name TEXT,"
        "rarity INTEGER"
        ")"
        "STRICT"
    )


def insert_data_primary(conn: sqlite3.Connection):
    cursor = conn.cursor()
    conn_fsearch = db_connect("fsearch")
    cursor_fsearch = conn_fsearch.cursor()
    relics_name_id = cursor_fsearch.execute("SELECT id FROM relics_name")
    data_relic_primary = []
    for relic_id in relics_name_id:
        id: int = relic_id[0]
        id_relic: int = Relic(id).id()
        name: str = Relic(id).name()
        rarity: int = Relic(id).rarity()
        data_relic_primary.append({"id": id_relic, "name": name, "rarity": rarity})
    Q_INSERT_INTO_RELIC_PRIMARY = """INSERT OR IGNORE INTO relics(
    relic_id,
    name,
    rarity
    ) VALUES(
    :id,
    :name,
    :rarity
    )
    """

    cursor.executemany(Q_INSERT_INTO_RELIC_PRIMARY, data_relic_primary)
    conn.commit()


def create_table_set_bonus(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relic_set_bonus("
        "p_key INTEGER PRIMARY KEY,"
        "relic_id INTEGER,"
        "use_num INTEGER,"
        "descHash TEXT,"
        "FOREIGN KEY(relic_id) REFERENCES relics(relic_id)"
        ")"
        "STRICT"
    )


def insert_data_set_bonus(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute("SELECT relic_id from relics")
    data_set_bonus = []
    for id in cursor:
        set_bonus_data = Relic(id[0]).set_bonus()
        for bonus in set_bonus_data:
            relic_id: int = id[0]
            use_num: int = bonus[0]
            p_key_setbonus: int = int(str(use_num) + str(relic_id))
            desc_hash: str = bonus[1]
            data_set_bonus.append(
                {
                    "p_key": p_key_setbonus,
                    "id": relic_id,
                    "useNum": use_num,
                    "descHash": desc_hash,
                }
            )
    Q_INSERT_INTO_SET_BONUS = """INSERT OR IGNORE INTO relic_set_bonus(
    p_key,
    relic_id,
    use_num,
    descHash
    ) VALUES(
    :p_key,
    :id,
    :useNum,
    :descHash
    )
    """
    cursor.executemany(Q_INSERT_INTO_SET_BONUS, data_set_bonus)
    conn.commit()


def create_table_main_stat(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relic_main_stat("
        "p_key INTEGER PRIMARY KEY,"
        "relic_id INTEGER,"
        "name TEXT,"
        "rarity INTEGER,"
        "baseTypeText TEXT,"
        "max_level INTEGER,"
        "main_affixes TEXT,"
        "FOREIGN KEY(relic_id) REFERENCES relics(relic_id)"
        ")"
        "STRICT"
    )


def insert_data_main_stat(conn: sqlite3.Connection):
    cursor = conn.cursor()
    relic_ids = cursor.execute("SELECT relic_id FROM relics")
    data_main_stat = []
    for relic_id in relic_ids:
        id: int = relic_id[0]
        main_stat = Relic(id).main_stat()
        baseTypeText_dict: dict = Relic(id).embeddedBaseTypes()
        for stat in main_stat:
            rarity: int = stat.get("rarity")
            name: str = stat.get("name")
            piece_part: str = stat.get("baseTypeText")
            baseTypeText_id = baseTypeText_dict.get(piece_part)
            max_level: int = stat.get("maxLevel")
            p_key_mainstat: int = int(str(baseTypeText_id) + str(id))
            main: list[dict] = stat.get("mainAffixes")
            data_main_stat.append(
                {
                    "p_key": p_key_mainstat,
                    "relic_id": id,
                    "rarity": rarity,
                    "name": name,
                    "baseTypeText": piece_part,
                    "maxLevel": max_level,
                    "mainAffixes": json.dumps(main),
                }
            )
    Q_INSERT_INTO_RELIC_MAIN_STAT = """INSERT OR IGNORE INTO relic_main_stat(
    p_key,
    relic_id,
    name,
    rarity,
    baseTypeText,
    max_level,
    main_affixes
    ) VALUES(
    :p_key,
    :relic_id,
    :name,
    :rarity,
    :baseTypeText,
    :maxLevel,
    :mainAffixes
    )
    """
    cursor.executemany(Q_INSERT_INTO_RELIC_MAIN_STAT, data_main_stat)
    conn.commit()


def create_table_sub_stat(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relic_sub_stat("
        "p_key INTEGER PRIMARY KEY, "
        "relic_id INTEGER, "
        "name TEXT, "
        "is_percent INTEGER, "
        "baseTypeText TEXT, "
        "rarity INTEGER , "
        "property_name TEXT,"
        "property_iconpath TEXT, "
        "base_value REAL, "
        "level_add REAL, "
        "step_value REAL, "
        "CHECK (is_percent = 0 OR is_percent = 1),"
        "FOREIGN KEY(relic_id) REFERENCES relics(relic_id)"
        ")"
        "STRICT"
    )


def insert_data_sub_stat(conn: sqlite3.Connection):
    cursor = conn.cursor()
    relic_ids = cursor.execute("SELECT relic_id FROM relics")
    data_sub_stat = []
    for relic_id in relic_ids:
        id: int = relic_id[0]
        sub_stat = Relic(id).sub_stat()
        baseTypeText_parts = Relic(id).embeddedBaseTypes()
        for stat in sub_stat:
            id_relic: int = id
            name: str = stat.get("name")
            is_percent_bool: bool = stat.get("isPercent")
            if is_percent_bool:
                is_percent = 1
            else:
                is_percent = 0
            basetypetext: str = stat.get("baseTypeText")
            baseTypeText_id: int = baseTypeText_parts.get(basetypetext)
            p_key_substat: int = int(str(baseTypeText_id) + str(id_relic))
            rarity: int = stat.get("rarity")
            property_name: str = stat.get("propertyName")
            property_iconpath: str = stat.get("propertyIconPath")
            base_value = float(stat.get("baseValue"))
            level_add = float(stat.get("levelAdd"))
            step_value: float = stat.get("stepValue")
            data_sub_stat.append(
                {
                    "p_key": p_key_substat,
                    "relic_id": id_relic,
                    "name": name,
                    "is_percent": is_percent,
                    "baseTypeText": basetypetext,
                    "rarity": rarity,
                    "property_name": property_name,
                    "property_iconpath": property_iconpath,
                    "base_value": base_value,
                    "level_add": level_add,
                    "step_value": step_value,
                }
            )

    Q_INSERT_INTO_SUB_STAT = """INSERT OR IGNORE INTO relic_sub_stat(
    p_key,
    relic_id, 
    name, 
    is_percent, 
    baseTypeText, 
    rarity, 
    property_name,
    property_iconpath, 
    base_value, 
    level_add, 
    step_value 
    ) VALUES(
    :p_key,
    :relic_id,
    :name,
    :is_percent,
    :baseTypeText,
    :rarity,
    :property_name,
    :property_iconpath,
    :base_value,
    :level_add,
    :step_value
    )
    """

    cursor.executemany(Q_INSERT_INTO_SUB_STAT, data_sub_stat)
    conn.commit()


if __name__ == "__main__":
    try:
        conn.close()
    except Exception:
        pass
