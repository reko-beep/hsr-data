import sqlite3
import json
from dotenv import dotenv_values
from data_query.relics_data import Relic

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
    Q_INSERT_INTO_RELIC_PRIMARY = """INSERT INTO relics(
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
    conn.close()


def create_table_set_bonus(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relic_set_bonus("
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
            relic_id = id[0]
            use_num = bonus[0]
            desc_hash = bonus[1]
            data_set_bonus.append(
                {"id": relic_id, "useNum": use_num, "descHash": desc_hash}
            )
    Q_INSERT_INTO_SET_BONUS = """INSERT INTO relic_set_bonus(
    relic_id,
    use_num,
    descHash
    ) VALUES(
    :id,
    :useNum,
    :descHash
    )
    """
    cursor.executemany(Q_INSERT_INTO_SET_BONUS, data_set_bonus)
    conn.commit()
    conn.close()


def create_table_main_stat(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS relic_main_stat("
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
        for stat in main_stat:
            rarity: int = stat.get("rarity")
            name: str = stat.get("name")
            piece_part: str = stat.get("baseTypeText")
            max_level: int = stat.get("maxLevel")
            main: list[dict] = stat.get("mainAffixes")
            data_main_stat.append(
                {
                    "relic_id": id,
                    "rarity": rarity,
                    "name": name,
                    "baseTypeText": piece_part,
                    "maxLevel": max_level,
                    "mainAffixes": json.dumps(main),
                }
            )
    Q_INSERT_INTO_RELIC_MAIN_STAT = """INSERT INTO relic_main_stat(
    relic_id,
    name,
    rarity,
    baseTypeText,
    max_level,
    main_affixes
    ) VALUES(
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
    conn.close()
