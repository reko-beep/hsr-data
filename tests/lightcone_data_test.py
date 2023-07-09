import unittest
from data_query.lightcones_data import LightCone
from typing import Generator, Tuple, List, Dict
from data_query.query_errors.errors import *
import data_query.shared_data.shared_var as SharedVar

test_lc = LightCone(20000)


class TestLightcones(unittest.TestCase):
    def test_json_data(self):
        self.assertEqual(isinstance(test_lc.json_data(), list), True)

    def test_name(self):
        name = "Arrows"
        self.assertEqual(test_lc.name(), name)

    def test_rarity(self):
        rarity = 3
        self.assertEqual(test_lc.rarity(), rarity)

    def test_level_data(self):
        self.assertEqual(isinstance(test_lc.level_data(), list), True)

    def test_level_data_onlevel(self):
        level_list = SharedVar.level()
        self.assertEqual(isinstance(test_lc.level_data_onlevel(), dict), True)
        for num in range(101):
            if num not in level_list:
                self.assertRaises(LevelOutOfRangeError, test_lc.level_data_onlevel, num)

    def test_skill_data(self):
        self.assertEqual(isinstance(test_lc.skill_data(), dict), True)

    def test_skill_data_onlevel(self):
        self.assertEqual(isinstance(test_lc.skill_data_onlevel(), dict), True)

    def test_skill_descHash(self):
        string = "Crisis Lv.5: At the start of the battle, the wearer's CRIT Rate increases by 24.0% for 3 turn(s)."
        self.assertEqual(test_lc.skill_descHash(), string)
        self.assertEqual(isinstance(test_lc.skill_descHash(), str), True)


if __name__ == "__main__":
    unittest.main()
