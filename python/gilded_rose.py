# -*- coding: utf-8 -*-

MAX_QUALITY = 50


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = {
                "Sulfuras, Hand of Ragnaros": LegendaryItemUpdater,
                "Aged Brie": AgedBrieUpdater,
                "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
            }.get(item.name, DefaultUpdater)
            updater.change_all(item)


class DefaultUpdater:
    def change_all(item):
        if item.quality > 0:
            item.quality = item.quality - 1

        item.sell_in = item.sell_in - 1

        if item.sell_in < 0:
            if item.quality > 0:
                item.quality = item.quality - 1


class LegendaryItemUpdater:
    def change_all(item):
        "Legendary items do not change in quality or sell-in time"
        pass


class AgedBrieUpdater:
    def change_all(item):
        if item.quality < MAX_QUALITY:
            item.quality = item.quality + 1

        item.sell_in = item.sell_in - 1

        if item.sell_in < 0:
            if item.quality < MAX_QUALITY:
                item.quality = item.quality + 1


class BackstagePassUpdater:
    def change_all(item):
        if item.quality < MAX_QUALITY:
            item.quality = item.quality + 1

            if item.quality < MAX_QUALITY:
                if item.sell_in < 11:
                    item.quality = item.quality + 1
                if item.sell_in < 6:
                    item.quality = item.quality + 1

        item.sell_in = item.sell_in - 1

        if item.sell_in < 0:
            item.quality = item.quality - item.quality


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
