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

def create_db():
    fsearch_books.create_table_books(fsearch_db)
    fsearch_char.create_table(fsearch_db)
    fsearch_food.create_table_foods(fsearch_db)
    fsearch_lc.create_table(fsearch_db)
    fsearch_mats.create_table(fsearch_db)
    fsearch_relics.create_table(fsearch_db)

if __name__ == "__main__":
    create_db()