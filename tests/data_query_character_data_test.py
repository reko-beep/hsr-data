import unittest
from itertools import count
from data_query.character_data import Character
from typing import Generator, Tuple, List, Dict
from data_query.query_errors.error_msg import QueryError

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
        level_iterator = count(start=20, step=10)
        level_list: List = list(next(level_iterator) for _ in range(7))
        stat_data_onlevel_20 = test_char.stat_data_onlevel(20)
        self.assertEqual(isinstance(stat_data_onlevel_20, Dict), True)
        for num in range(101):
            if num not in level_list:
                stat_data_onlevel_error = test_char.stat_data_onlevel(num)
                self.assertEqual(stat_data_onlevel_error, QueryError.leveldata_outofrange())
        stat_data_onlevel_error_notint = test_char.stat_data_onlevel("potato")
        self.assertEqual(stat_data_onlevel_error_notint, QueryError.leveldata_outofrange())
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

if __name__ == '__main__':
    unittest.main()
