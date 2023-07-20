import data_query.fsearch.books_names_db as fsearch_books
import data_query.fsearch.char_names_db as fsearch_char
import data_query.fsearch.food_names_db as fsearch_food
import data_query.fsearch.lc_names_db as fsearch_lc
import data_query.fsearch.mats_names_db as fsearch_mats
import data_query.fsearch.relics_name_db as fsearch_relics
import sqlite3
import os
from dotenv import dotenv_values
from pathlib import Path

os.chdir(Path(__file__).parent.parent.parent)
key = dotenv_values(".env")
fsearch_db = sqlite3.connect(key["FSEARCH_DB"])


def update_db():
    fsearch_books.insert_data_books(fsearch_db)
    fsearch_char.insert_data_names(fsearch_db)
    fsearch_food.insert_data_food(fsearch_db)
    fsearch_lc.insert_data_lightcones(fsearch_db)
    fsearch_mats.insert_data_materials(fsearch_db)
    fsearch_relics.insert_data_relics(fsearch_db)
    fsearch_db.close()


if __name__ == "__main__":
    update_db()
