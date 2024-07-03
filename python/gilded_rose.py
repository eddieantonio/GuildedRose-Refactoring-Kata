# -*- coding: utf-8 -*-


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            update_item_quality(item)


class DefaultUpdater:
    @staticmethod
    def apply_initial_quality_change(item):
        if item.quality > 0:
            item.quality = item.quality - 1

    @staticmethod
    def reduce_sell_by_date(item):
        item.sell_in = item.sell_in - 1

    @staticmethod
    def adjust_quality_post_sell_date(item):
        if item.quality > 0:
            item.quality = item.quality - 1


class AgedBrieUpdater(DefaultUpdater):
    @staticmethod
    def apply_initial_quality_change(item):
        if item.quality < 50:
            item.quality = item.quality + 1

    def adjust_quality_post_sell_date(item):
        if item.quality < 50:
            item.quality = item.quality + 1


class BackstagePassUpdater(DefaultUpdater):
    @staticmethod
    def apply_initial_quality_change(item):
        if item.quality < 50:
            item.quality = item.quality + 1
            if item.sell_in < 11:
                if item.quality < 50:
                    item.quality = item.quality + 1
            if item.sell_in < 6:
                if item.quality < 50:
                    item.quality = item.quality + 1

    def adjust_quality_post_sell_date(item):
        item.quality = item.quality - item.quality


class SulfurasHandOfRaggnarosUpdater(DefaultUpdater):
    @staticmethod
    def apply_initial_quality_change(item):
        "Legendary item does not decrease in quality."
        pass

    @staticmethod
    def reduce_sell_by_date(item):
        "Legendary item does not decrease its sell-in date."
        pass

    @staticmethod
    def adjust_quality_post_sell_date(item):
        pass


def update_item_quality(item):
    """
    Apply the update rule for the day.
    """

    updater = {
        "Backstage passes to a TAFKAL80ETC concert": BackstagePassUpdater,
        "Aged Brie": AgedBrieUpdater,
        "Sulfuras, Hand of Ragnaros": SulfurasHandOfRaggnarosUpdater,
    }.get(item.name, DefaultUpdater)

    # Apply quality change
    updater.apply_initial_quality_change(item)

    # Apply sell_by change
    updater.reduce_sell_by_date(item)

    # Adjust quality after sell by date
    if item.sell_in < 0:
        # We need to sell it!
        updater.adjust_quality_post_sell_date(item)


def is_item_that_appreciates(item):
    return (
        item.name == "Aged Brie"
        or item.name == "Backstage passes to a TAFKAL80ETC concert"
    )


class Item:
    def __init__(self, name, sell_in, quality):
        self.name = name
        self.sell_in = sell_in
        self.quality = quality

    def __repr__(self):
        return "%s, %s, %s" % (self.name, self.sell_in, self.quality)
