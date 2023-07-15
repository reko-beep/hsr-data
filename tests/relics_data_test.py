import unittest
from data_query.relics_data import Relic

test_relic = Relic(101)


class TestRelics(unittest.TestCase):
    def test_name(self):
        self.assertEqual(test_relic.name(), "Passerby of Wandering Cloud")

    def test_id(self):
        self.assertEqual(test_relic.id(), 101)

    def test_rarity(self):
        rarity = 5
        self.assertEqual(test_relic.rarity(), rarity)
    def test_set_bonus(self):
        for data in test_relic.set_bonus():
            self.assertEqual(isinstance(data, tuple), True)

    def test_pieces_effect_data(self):
        self.assertEqual(isinstance(test_relic.pieces_effect_data(), list), True)

    def test_main_stat(self):
        for data in test_relic.main_stat():
            self.assertEqual(isinstance(data, dict), True)

    def test_sub_stat(self):
        for data in test_relic.sub_stat():
            self.assertEqual(isinstance(data, dict), True)


if __name__ == "__main__":
    unittest.main()
