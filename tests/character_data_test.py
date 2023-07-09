import unittest
from itertools import count
from data_query.character_data import Character
from typing import Generator
from data_query.query_errors.errors import *
import data_query.shared_data.shared_var as SharedVar

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
        self.assertEqual(isinstance(test_char.stat_data_onlevel(20), dict), True)
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
            self.assertEqual(isinstance(data, tuple), True)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0] is not None, True)
            self.assertEqual(data[1] is not None, True)

    def test_stat_at_max(self):
        content = test_char.stat_at_max()
        self.assertEqual(isinstance(content, dict), True)

    def test_skills(self):
        skills_data = test_char.get_skill_data()
        self.assertEqual(isinstance(skills_data, list), True)

    def test_trace(self):
        for data in test_char.trace():
            self.assertEqual(isinstance(data, dict), True)

    def test_constellation(self):
        for data in test_char.constellation():
            self.assertEqual(isinstance(data, str), True)

    def test_skills(self):
        self.assertEqual(test_char.name(), "Arlan")

        self.assertEqual(
            test_char.skill_basicatk(),
            "Basic ATK Lv.9: Deals Lightning DMG equal to 130.0% of Arlan's ATK to a single enemy.",
        )

        self.assertEqual(
            test_char.skill_skill(),
            "Skill Lv.15: Consumes Arlan's HP equal to 15.0% of his Max HP to deal Lightning DMG equal to 3% of Arlan's ATK to a single enemy. If Arlan does not have sufficient HP, his HP will be reduced to 1 after using his Skill.",
        )

        self.assertEqual(
            test_char.skill_talent(),
            "Talent Lv.15: Increases Arlan's DMG for every percent of HP below his Max HP, up to a max of 90.0% more DMG.",
        )
        self.assertEqual(
            test_char.skill_ultimate(),
            "Ultimate Lv.15: Deals Lightning DMG equal to 384.0% of Arlan's ATK to a single enemy and Lightning DMG equal to 192.0% of Arlan's ATK to enemies adjacent to it.",
        )
        self.assertEqual(
            test_char.skill_technique(),
            "Technique Lv.1: Immediately attacks the enemy. After entering battle, deals Lightning DMG equal to 80.0% of Arlan's ATK to all enemies.",
        )


if __name__ == "__main__":
    unittest.main()
