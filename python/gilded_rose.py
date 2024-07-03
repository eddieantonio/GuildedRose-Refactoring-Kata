# -*- coding: utf-8 -*-

MAX_QUALITY = 50


class GildedRose(object):
    def __init__(self, items):
        self.items = items

    def update_quality(self):
        for item in self.items:
            apply_policy, change_in_quality = determine_policy(item.name)
            apply_policy(item, change_in_quality)


def determine_policy(item_name):
    apply_policy, change_in_quality = {
        "Sulfuras, Hand of Ragnaros": (legendary_item_change_policy, ...),
        "Aged Brie": (default_change_policy, better_with_age_change_in_quality),
        "Backstage passes to a TAFKAL80ETC concert": (
            default_change_policy,
            backstage_pass_change_in_quality,
        ),
    }.get(item_name, (default_change_policy, default_change_in_quality))

    if item_name.startswith("Conjured "):
        change_in_quality = decorate_with_double(change_in_quality)

    return apply_policy, change_in_quality


def default_change_policy(item, change_in_quality):
    item.sell_in -= 1
    change = change_in_quality(item)
    item.quality = clamp(item.quality + change, lower=0, upper=MAX_QUALITY)


def legendary_item_change_policy(item, _change_in_quality):
    "Legendary items do not change in quality or sell-in time"
    pass


def default_change_in_quality(item):
    if item.sell_in >= 0:
        return -1
    else:
        return -2


def better_with_age_change_in_quality(item):
    if item.sell_in >= 0:
        return +1
    else:
        return +2


def backstage_pass_change_in_quality(item):
    if item.sell_in < 0:
        return -item.quality
    elif item.sell_in < 5:
        return +3
    elif item.sell_in < 10:
        return +2
    else:
        return +1


def decorate_with_double(original_change_in_quality):
    def change_in_quality(item):
        return 2 * original_change_in_quality(item)

    return change_in_quality


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
