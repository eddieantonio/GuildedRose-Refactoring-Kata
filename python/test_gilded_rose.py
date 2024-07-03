# -*- coding: utf-8 -*-
import unittest

from gilded_rose import GildedRose, Item


class GildedRoseTest(unittest.TestCase):
    def test_ordinary_item(self):
        items = [Item("Plain ol' Grog", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Plain ol' Grog", items[0].name)
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(9, items[0].quality)

    def test_charmed_item(self):
        items = [Item("Charmed Grog", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Charmed Grog", items[0].name)
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(8, items[0].quality)

    def test_charmed_brie(self):
        items = [Item("Charmed Aged Brie", 1, 10)]
        gilded_rose = GildedRose(items)
        gilded_rose.update_quality()
        self.assertEqual("Charmed Aged Brie", items[0].name)
        self.assertEqual(0, items[0].sell_in)
        self.assertEqual(6, items[0].quality)


if __name__ == "__main__":
    unittest.main()
