# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            updater = {
                "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
                "Aged Brie": AgedBrieUpdater,
                "Sulfuras, Hand of Ragnaros": LegendaryItemUpdater,
            }.get(item.name, DefaultUpdater)

            # Apply quality change
            updater.apply_initial_quality_change(item)

            # Apply sell_by change
            updater.reduce_sell_by_date(item)

            # Adjust quality after sell by date
            if item.sell_in < 0:
                # We need to sell it!
                updater.adjust_quality_post_sell_date(item)


class DefaultUpdater:
    def apply_initial_quality_change(item):
        if item.quality > 0:
            item.quality = item.quality - 1

    def reduce_sell_by_date(item):
        item.sell_in = item.sell_in - 1

    def adjust_quality_post_sell_date(item):
        if item.quality > 0:
            item.quality = item.quality - 1


class AgedBrieUpdater(DefaultUpdater):
    def apply_initial_quality_change(item):
        if item.quality < 50:
            item.quality = item.quality + 1

    def adjust_quality_post_sell_date(item):
        if item.quality < 50:
            item.quality = item.quality + 1


class BackstagePassUpdater(DefaultUpdater):
    def apply_initial_quality_change(item):
        if item.quality >= 50:
            return

        item.quality = item.quality + 1
        if item.sell_in < 11:
            if item.quality < 50:
                item.quality = item.quality + 1
        if item.sell_in < 6:
            if item.quality < 50:
                item.quality = item.quality + 1

    def adjust_quality_post_sell_date(item):
        item.quality = item.quality - item.quality


class LegendaryItemUpdater(DefaultUpdater):
    "Legendary items do not change in quality, nor do they need to be sold by any date."

    def apply_initial_quality_change(item):
        pass

    def reduce_sell_by_date(item):
        pass

    def adjust_quality_post_sell_date(item):
        pass


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
