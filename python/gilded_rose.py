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
            if item.name.startswith("Charmed "):
                updater = decorate_charmed_item(updater)

            updater.change_all(item)


class DefaultUpdater:
    @classmethod
    def change_all(cls, item):
        item.sell_in -= 1
        change = cls.change_in_quality(item)
        item.quality = clamp(item.quality + change, lower=0, upper=MAX_QUALITY)

    @classmethod
    def change_in_quality(cls, item):
        if item.sell_in >= 0:
            return -1
        else:
            return -2


class LegendaryItemUpdater:
    def change_all(item):
        "Legendary items do not change in quality or sell-in time"
        pass


class AgedBrieUpdater(DefaultUpdater):
    @classmethod
    def change_in_quality(cls, item):
        if item.sell_in >= 0:
            return +1
        else:
            return +2


class BackstagePassUpdater(DefaultUpdater):
    @classmethod
    def change_in_quality(cls, item):
        if item.sell_in < 0:
            return -item.quality
        elif item.sell_in < 5:
            return +3
        elif item.sell_in < 10:
            return +2
        else:
            return +1


def decorate_charmed_item(original_updater):
    class CharmedItemUpdater(DefaultUpdater):
        @classmethod
        def change_in_quality(cls, item):
            return 2 * original_updater.change_in_quality(item)

    return CharmedItemUpdater


def clamp(value, *, lower=float("-inf"), upper=float("inf")):
    "Clamp the value to given inclusive range."
    return max(lower, min(upper, value))


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
