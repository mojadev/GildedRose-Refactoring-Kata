
# -*- coding: utf-8 -*-

AGED_BRIE = "Aged Brie"
BACKSTAGE_PASS = "Backstage passes to a TAFKAL80ETC concert"
SULFURAS = "Sulfuras, Hand of Ragnaros"

UPPER_RANGE = 50
LOWER_RANGE = 0
class GildedRose(object):

    def __init__(self, items):
        self.items = items
        self.item_handler = {
            SULFURAS: handle_sulfuras,
            BACKSTAGE_PASS: handle_backstage_pass,
            AGED_BRIE: handle_aged_brie
        }

    def update_single_item(self, item):        
        item.sell_in -= 1
        if item.name in self.item_handler:
            self.item_handler[item.name](item)
        else:
            handle_normal_item(item)

    def update_quality(self):
        for item in self.items:
            self.update_single_item(item)


def is_conjured(item):
    return "conjured" in item.name.lower()


def handle_sulfuras(item):
    item.sell_in += 1
    item.quality = 80;


def handle_normal_item(item):
    quality_factor = find_quality_factor(item)
    if is_conjured(item):
        quality_factor *= 2
    update_item_quality(item, quality_factor) 


def handle_aged_brie(item):
    quality_factor = -1 * find_quality_factor(item)
    update_item_quality(item, quality_factor) 
    

def handle_backstage_pass(item):
    quality_factor = 1
    if item.sell_in < 10:
        quality_factor += 1
    if item.sell_in < 5:
        quality_factor += 1
    
    update_item_quality(item, quality_factor)
    if item.sell_in < 0:
        item.quality = LOWER_RANGE


def update_item_quality(item, step =1):
    item.quality += step
    if item.quality > UPPER_RANGE:
        item.quality = UPPER_RANGE
    if item.quality < LOWER_RANGE:
        item.quality = LOWER_RANGE
    

def find_quality_factor(item):
    quality_factor = -1
    if (item.sell_in < 0):
        quality_factor *= 2
    return quality_factor

class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
