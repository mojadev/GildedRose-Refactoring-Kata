# -*- coding: utf-8 -*-
import unittest

from gilded_rose import Item, GildedRose

# Not clearly defined in requirements
EXPECTED_QUALITY_DROP = 1
EXPECTED_SELLIN_DROP = 1

INITIAL_VALUE = 10
INITIAL_SELL_IN = 5
INITIAL_BACKSTAGE_SELLIN = 20
SULFURAS_VALUE = 80

class GildedRoseTest(unittest.TestCase):

    @property
    def normal_item(self):
        return Item("normal_item", INITIAL_SELL_IN, INITIAL_VALUE)

    @property
    def aged_brie(self):
        return Item("Aged Brie", INITIAL_SELL_IN, INITIAL_VALUE)
    
    @property
    def sulfuras(self):
        return Item("Sulfuras, Hand of Ragnaros", INITIAL_SELL_IN, SULFURAS_VALUE)

    @property
    def backstage_passes(self):
        return Item("Backstage passes to a TAFKAL80ETC concert", INITIAL_BACKSTAGE_SELLIN, INITIAL_VALUE)


    def test_normal_item_decreases_after_one_day(self):
        current_item = self.normal_item;
        gilded_rose = GildedRose([current_item])

        gilded_rose.update_quality()

        self.assertLess(current_item.quality, self.normal_item.quality)
        self.assertEqual(current_item.quality, self.normal_item.quality - EXPECTED_QUALITY_DROP)


    def test_sellin_decreases_after_one_day(self):
        normal_item = self.normal_item
        gilded_rose = GildedRose([normal_item])

        gilded_rose.update_quality()

        self.assertEqual(normal_item.sell_in, self.normal_item.sell_in - EXPECTED_SELLIN_DROP)


    def test_sellin_reached__normal_item_decreases_twice_as_fast(self):
        current_item = self.normal_item
        gilded_rose = GildedRose([current_item])

        current_item.sell_in = 0
        gilded_rose.update_quality()

        self.assertEqual(current_item.quality, self.normal_item.quality - EXPECTED_QUALITY_DROP * 2)


    def test_quality_is_never_negative(self):
        current_item = self.normal_item
        gilded_rose = GildedRose([current_item])

        current_item.quality = 0
        gilded_rose.update_quality()

        self.assertEqual(current_item.quality, 0)


    def xtest_quality_is_never_negative__negative_default(self):
        current_item = self.normal_item
        gilded_rose = GildedRose([current_item])

        current_item.quality = -1
        gilded_rose.update_quality()

        self.assertEqual(current_item.quality, 0)


    def test_aged_brie_quality_increases(self):
        aged_brie = self.aged_brie
        gilded_rose = GildedRose([aged_brie])

        gilded_rose.update_quality()

        self.assertEqual(aged_brie.quality, self.aged_brie.quality + EXPECTED_QUALITY_DROP)


    def test_sellin_less_than_0__aged_brie_quality_increases_twice_as_fast(self):
        aged_brie = self.aged_brie
        gilded_rose = GildedRose([aged_brie])

        aged_brie.sell_in = -1;
        gilded_rose.update_quality()

        self.assertEqual(aged_brie.quality, self.aged_brie.quality + EXPECTED_QUALITY_DROP * 2)


    def test_sellin_less_than_0__aged_brie_quality_cannot_increase_to_51(self):
        aged_brie = self.aged_brie
        gilded_rose = GildedRose([aged_brie])

        aged_brie.quality = 49
        aged_brie.sell_in = -1
        gilded_rose.update_quality()

        self.assertEqual(aged_brie.quality, 50)


    def test_quality_is_never_higher_than_50(self):
        aged_brie = self.aged_brie
        gilded_rose = GildedRose([aged_brie])

        aged_brie.quality = 49
        for x in range(3):
            gilded_rose.update_quality()
        
        self.assertEqual(aged_brie.quality, 50)


    def test_sulfuras_quality_stays_the_same(self):
        sulfuras = self.sulfuras
        gilded_rose = GildedRose([sulfuras])

        for x in range(3):
            gilded_rose.update_quality()
        
        self.assertEqual(sulfuras.quality, SULFURAS_VALUE)


    def test_sulfuras_sellin_stays_the_same(self):
        sulfuras = self.sulfuras
        gilded_rose = GildedRose([sulfuras])

        for x in range(3):
            gilded_rose.update_quality()
        
        self.assertEqual(sulfuras.sell_in, INITIAL_SELL_IN)


    def test_sulfuras_sellin_reached__value_stays_the_same(self):
        sulfuras = self.sulfuras
        gilded_rose = GildedRose([sulfuras])

        sulfuras.sell_in = -1
        for x in range(3):
            gilded_rose.update_quality()
        
        self.assertEqual(sulfuras.quality, SULFURAS_VALUE)


    def test_sellin_more_than_10__backstage_passes_quality_increases_by_1(self):
        backstage_passes = self.backstage_passes
        gilded_rose = GildedRose([backstage_passes])

        backstage_passes.sell_in = 20
        for x in range(1, 11):
            gilded_rose.update_quality()
            self.assertEqual(backstage_passes.quality, self.backstage_passes.quality + x)


    def test_sellin_more_than_5_less_than_10__backstage_passes_quality_increases_by_2(self):
        backstage_passes = self.backstage_passes
        gilded_rose = GildedRose([backstage_passes])

        backstage_passes.sell_in = 10
        for x in range(1, 6):
            gilded_rose.update_quality()
            self.assertEqual(backstage_passes.quality, self.backstage_passes.quality + 2 *  x)


    def test_sellin_less_than_5__backstage_passes_quality_increases_by_3(self):
        backstage_passes = self.backstage_passes
        gilded_rose = GildedRose([backstage_passes])

        backstage_passes.sell_in = 5
        for x in range(1, 6):
            gilded_rose.update_quality()
            self.assertEqual(backstage_passes.quality, self.backstage_passes.quality + 3 * x)


    def test_sellin_0__backstage_passes_quality_becomes_0(self):
        backstage_passes = self.backstage_passes
        gilded_rose = GildedRose([backstage_passes])

        backstage_passes.sell_in = 0
        gilded_rose.update_quality()

        self.assertEqual(backstage_passes.quality, 0)


    def test_sellin_negative__backstage_passes_quality_becomes_0(self):
        backstage_passes = self.backstage_passes
        gilded_rose = GildedRose([backstage_passes])

        backstage_passes.sell_in = -10
        gilded_rose.update_quality()

        self.assertEqual(backstage_passes.quality, 0)


if __name__ == '__main__':
    unittest.main()
