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
    @classmethod
    def change_all(cls, item):
        item.sell_in = cls.new_sell_in(item)
        item.quality = max(0, min(MAX_QUALITY, cls.new_quality(item)))

    @classmethod
    def new_sell_in(cls, item):
        return item.sell_in - 1

    @classmethod
    def new_quality(cls, item):
        if item.sell_in >= 0:
            return item.quality - 1
        else:
            return item.quality - 2


class LegendaryItemUpdater:
    def change_all(item):
        "Legendary items do not change in quality or sell-in time"
        pass


class AgedBrieUpdater(DefaultUpdater):
    @classmethod
    def new_quality(cls, item):
        if item.sell_in >= 0:
            return item.quality + 1
        else:
            return item.quality + 2


class BackstagePassUpdater(DefaultUpdater):
    @classmethod
    def new_quality(cls, item):
        if item.sell_in < 0:
            return 0
        elif item.sell_in < 5:
            return item.quality + 3
        elif item.sell_in < 10:
            return item.quality + 2
        else:
            return item.quality + 1


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
