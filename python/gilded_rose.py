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
            }.get(item.name, DefaultUpdater)()
            if item.name.startswith("Charmed "):
                updater = CharmedUpdaterDecorator(updater)
            updater.change_all(item)


class DefaultUpdater:
    def change_all(self, item):
        item.sell_in -= 1
        change = self.change_in_quality(item)
        item.quality = clamp(item.quality + change, lower=0, upper=MAX_QUALITY)

    def change_in_quality(self, item):
        if item.sell_in >= 0:
            return -1
        else:
            return -2


class LegendaryItemUpdater:
    def change_all(self, item):
        "Legendary items do not change in quality or sell-in time"
        pass


class AgedBrieUpdater(DefaultUpdater):
    def change_in_quality(self, item):
        if item.sell_in >= 0:
            return +1
        else:
            return +2


class BackstagePassUpdater(DefaultUpdater):
    def change_in_quality(self, item):
        if item.sell_in < 0:
            return -item.quality
        elif item.sell_in < 5:
            return +3
        elif item.sell_in < 10:
            return +2
        else:
            return +1


class CharmedUpdaterDecorator(DefaultUpdater):
    def __init__(self, updater):
        self._wrapped = updater

    def change_in_quality(self, item):
        return 2 * self._wrapped.change_in_quality(item)


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
