import unittest
import sqlite3 as sql
from data_query.materials_data import Materials
from dotenv import dotenv_values


key = dotenv_values(".env")
conn = sql.connect(key["FSEARCH_DB"])


class TestMaterials(unittest.TestCase):
    def test_name(self):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name from mats_names")
        for mats_id, name in cursor:
            self.assertEqual(Materials(mats_id).name(), name)

    def test_id(self):
        cursor = conn.cursor()
        cursor.execute("SELECT id, name from mats_names")
        for mats_id, name in cursor:
            self.assertEqual(Materials(mats_id).id(), mats_id)

    def test_rarity(self):
        cursor = conn.cursor()
        cursor.execute("SELECT id, rarity from mats_names")
        for mats_id, rarity in cursor:
            self.assertEqual(Materials(mats_id).rarity(), rarity)


if __name__ == "__main__":
    unittest.main()
