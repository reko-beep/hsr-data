import unittest
from itertools import count
from data_query.character_data import Character
from typing import Generator, Tuple, List, Dict
from data_query.query_errors.errors import *
from data_query.shared_data.shared_var import SharedVar

char_name = "arlan"
test_char = Character(char_name)


class TestCharacter(unittest.TestCase):
    def test_json_data(self):
        json_data = test_char.json_data()
        for i in json_data:
            self.assertEqual(isinstance(i, str), True)  # add assertion here

    def test_name(self):
        name = test_char.name()
        self.assertEqual(isinstance(name, str), True)
        self.assertEqual(name.title(), char_name.title())

    def test_damage_type(self):
        dmg_type = test_char.damage_type()
        self.assertEqual(isinstance(dmg_type, str), True)
        self.assertEqual(dmg_type, "Lightning")

    def test_path(self):
        path = test_char.path()
        self.assertEqual(isinstance(path, str), True)
        self.assertEqual(path, "Destruction")

    def test_stat_data_onlevel(self):
        level_list: List[int] = SharedVar.level()
        stat_data_onlevel_20 = test_char.stat_data_onlevel(20)
        self.assertEqual(isinstance(test_char.stat_data_onlevel(20), Dict), True)
        for num in range(101):
            if num not in level_list:
                self.assertRaises(
                    LevelOutOfRangeError, test_char.stat_data_onlevel, num
                )
        self.assertRaises(LevelOutOfRangeError, test_char.stat_data_onlevel, "potato")

    def test_stat_data_max(self):
        stat_data_max = test_char.stat_data_max()
        self.assertEqual(isinstance(stat_data_max, Generator), True)
        for data in stat_data_max:
            self.assertEqual(isinstance(data, Tuple), True)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0] is not None, True)
            self.assertEqual(data[1] is not None, True)

    def test_stat_at_max(self):
        content = test_char.stat_at_max()
        self.assertEqual(isinstance(content, Dict), True)

    def test_skills(self):
        skills_data = test_char.skills()
        self.assertEqual(isinstance(skills_data, Dict), True)

    def test_trace(self):
        for data in test_char.trace():
            self.assertEqual(isinstance(data, dict), True)

    def test_constellation(self):
        for data in test_char.constellation():
            self.assertEqual(isinstance(data, tuple), True)

if __name__ == "__main__":
    unittest.main()
