import sqlite3 as sql
from dotenv import dotenv_values

key = dotenv_values(".env")


def db_connect():
    return sql.connect(key["HSR_DB_LOCATION"])
