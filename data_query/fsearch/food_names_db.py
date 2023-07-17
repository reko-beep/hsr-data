import sqlite3
import os
from data_query.foods_data import Foods
from pathlib import Path
from dotenv import dotenv_values

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")

conn = sqlite3.connect(key["FSEARCH_DB"])


def create_table_foods(conn: sqlite3.Connection):
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS foods_names("
        "id INTEGER PRIMARY KEY,"
        "name TEXT,"
        "rarity INTEGER"
        ")"
    )


def insert_data_food(conn: sqlite3.Connection):
    cursor = conn.cursor()
    filenames: list[int] = [
        int(filename.replace(".json", ""))
        for filename in os.listdir("raw_data/en/foods")
        if ".json" in filename
    ]
    data_foods = []
    for id in filenames:
        foods = Foods(id)
        name: str = foods.name()
        foods_id: int = foods.food_id()
        rarity: int = foods.rarity()
        data_foods.append({"name": name, "id": foods_id, "rarity": rarity})

    Q_INSERT_INTO_FOODS_FSEARCH = """INSERT INTO foods_names(
    id,
    name,
    rarity
    ) VALUES(
    :id,
    :name,
    :rarity
    )
    """
    cursor.executemany(Q_INSERT_INTO_FOODS_FSEARCH, data_foods)
    conn.commit()
    conn.close()
