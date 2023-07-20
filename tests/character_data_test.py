import unittest
import sqlite3
import data_query.shared_data.shared_var as SharedVar
from itertools import count
from data_query.character_data import Character
from typing import Generator
from data_query.query_errors.errors import *
from dotenv import dotenv_values

char_name = "arlan"
test_char = Character(char_name)
key = dotenv_values(".env")


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

    def test_skills(self):
        skills_data = test_char.get_skill_data()
        self.assertEqual(isinstance(skills_data, list), True)

    def test_trace(self):
        data = test_char.trace()
        self.assertEqual(isinstance(data, dict), True)
        conn = sqlite3.connect(key["FSEARCH_DB"])
        cursor = conn.cursor()
        cursor.execute("SELECT filename FROM char_names")
        for name in cursor:
            trace_data = Character(name[0]).trace()
            self.assertEqual(isinstance(trace_data, dict), True)
            print(trace_data)
        conn.close()

    def test_constellation(self):
        for data in test_char.constellation():
            self.assertEqual(isinstance(data, str), True)
            print(data)

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

        bailu = Character("bailu")

        self.assertEqual(
            bailu.skill_basicatk(),
            "Basic ATK Lv.9: Deals Lightning DMG equal to 130.0% of Bailu's ATK to a single enemy.",
        )
        self.assertEqual(
            bailu.skill_skill(),
            "Skill Lv.15: Heals a single ally for 13.7% of Bailu's Max HP plus 399.75. Bailu then heals random allies 2 time(s). After each healing, HP restored from the next healing is reduced by 15.0%.",
        )
        self.assertEqual(
            bailu.skill_talent(),
            "Talent Lv.15: After an ally with Invigoration is hit, restores the ally's HP for 6.3% of Bailu's Max HP plus 184.5. This effect can trigger 2 time(s). When an ally receives a killing blow, they will not be knocked down. Bailu immediately heals the ally for 21.0% of Bailu's Max HP plus 615 HP. This effect can be triggered 1 time per battle.",
        )
        self.assertEqual(
            bailu.skill_ultimate(),
            "Ultimate Lv.15: Heals all allies for 15.8% of Bailu's Max HP plus 461.25. Bailu applies Invigoration to allies that are not already Invigorated. For those already Invigorated, Bailu extends the duration of their Invigoration by 1 turn. The effect of Invigoration can last for 2 turn(s). This effect cannot stack.",
        )
        self.assertEqual(
            bailu.skill_technique(),
            "Technique Lv.1: After using Technique, at the start of the next battle, all allies are granted Invigoration for 2 turn(s).",
        )

        bronya = Character("bronya")

        self.assertEqual(
            bronya.skill_basicatk(),
            "Basic ATK Lv.9: Deals Wind DMG equal to 130.0% of Bronya's ATK to a single enemy.",
        )
        self.assertEqual(
            bronya.skill_skill(),
            "Skill Lv.15: Dispels a debuff from a single ally, allows them to immediately take action, and increases their DMG by 82.5% for 1 turn(s). When this Skill is used on Bronya herself, she cannot immediately take action again.",
        )
        self.assertEqual(
            bronya.skill_talent(),
            "Talent Lv.15: After using her Basic ATK, Bronya's next action will be Advanced Forward by 37.5%.",
        )
        self.assertEqual(
            bronya.skill_ultimate(),
            "Ultimate Lv.15: Increases the ATK of all allies by 66.0%, and increases their CRIT DMG equal to 18.0% of Bronya's CRIT DMG plus 24.0% for 2 turn(s).",
        )
        self.assertEqual(
            bronya.skill_technique(),
            "Technique Lv.1: After using Bronya's Technique, at the start of the next battle, all allies' ATK increases by 15.0% for 2 turn(s).",
        )

        pela = Character("pela")

        self.assertEqual(
            pela.skill_basicatk(),
            "Basic ATK Lv.9: Deals Ice DMG equal to 130.0% of Pela's ATK as to a single enemy.",
        )
        self.assertEqual(
            pela.skill_skill(),
            "Skill Lv.15: Removes 1 buff(s) and deals Ice DMG equal to 262.5% of Pela's ATK as to a single enemy.",
        )
        self.assertEqual(
            pela.skill_talent(),
            "Talent Lv.15: If the enemy is debuffed after Pela's attack, Pela will restore 12.5 extra Energy. This effect can only be triggered 1 time per attack.",
        )
        self.assertEqual(
            pela.skill_ultimate(),
            "Ultimate Lv.15: Deals Ice DMG equal to 120.0% of Pela's ATK to all enemies, with a 1% base chance to inflict Exposed on all enemies. When Exposed, enemies' DEF is reduced by 45.0% for 2 turn(s).",
        )
        self.assertEqual(
            pela.skill_technique(),
            "Technique Lv.1: Immediately attacks the enemy. Upon entering battle, Pela deals Ice DMG equal to 80.0% of her ATK to a random enemy, with a 1% base chance of lowering the DEF of all enemies by 20.0% for 2 turn(s).",
        )


if __name__ == "__main__":
    unittest.main()
