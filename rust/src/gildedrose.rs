use std::fmt::{self, Display};
pub struct Item {
    pub name: String,
    pub sell_in: i32,
    pub quality: i32,
}

impl Item {
    pub fn new(name: impl Into<String>, sell_in: i32, quality: i32) -> Item {
        Item {
            name: name.into(),
            sell_in,
            quality,
        }
    }
}

impl Display for Item {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        write!(f, "{}, {}, {}", self.name, self.sell_in, self.quality)
    }
}

pub struct GildedRose {
    pub items: Vec<Item>,
}

impl GildedRose {
    pub fn new(items: Vec<Item>) -> GildedRose {
        GildedRose { items }
    }

    pub fn update_quality(&mut self) {
        for item in self.items.iter_mut() {
            update_item(item)
        }
    }
}

fn update_item(item: &mut Item) {
    let is_aged_brie = item.name == "Aged Brie";
    let is_backstage_pass = item.name == "Backstage passes to a TAFKAL80ETC concert";
    let is_legendary = item.name == "Sulfuras, Hand of Ragnaros";

    if !is_aged_brie && !is_backstage_pass {
        if item.quality > 0 {
            if !is_legendary {
                item.quality -= 1;
            }
        }
    } else {
        if item.quality < 50 {
            item.quality += 1;

            if is_backstage_pass {
                if item.sell_in < 11 {
                    if item.quality < 50 {
                        item.quality += 1;
                    }
                }

                if item.sell_in < 6 {
                    if item.quality < 50 {
                        item.quality += 1;
                    }
                }
            }
        }
    }

    if !is_legendary {
        item.sell_in -= 1;
    }

    if item.sell_in < 0 {
        if !is_aged_brie {
            if !is_backstage_pass {
                if item.quality > 0 {
                    if !is_legendary {
                        item.quality -= 1;
                    }
                }
            } else {
                item.quality = 0;
            }
        } else {
            if item.quality < 50 {
                item.quality += 1;
            }
        }
    }
}


#[cfg(test)]
mod tests {
    use super::{GildedRose, Item};

    #[test]
    pub fn test_ordinary_item() {
        let items = vec![Item::new("Dull Dagger", 30, 10)];
        let mut rose = GildedRose::new(items);
        rose.update_quality();
        assert_eq!(29, rose.items[0].sell_in);
        assert_eq!(9, rose.items[0].quality);
    }

    #[test]
    pub fn test_ordinary_item_quality_doubles_past_sell_in_date() {
        let mut rose = GildedRose::new(vec![Item::new("Dull Dagger", -1, 10)]);
        rose.update_quality();
        assert_eq!(8, rose.items[0].quality);
        assert_eq!(-2, rose.items[0].sell_in);
    }

    #[test]
    pub fn test_ordinary_item_quality_cannot_decrease_past_zero() {
        let mut rose = GildedRose::new(vec![
            Item::new("Dull Dagger", 30, 0),
            Item::new("Adequate Wine (opened)", -1, 1),
        ]);
        rose.update_quality();
        assert_eq!(0, rose.items[0].quality);
        assert_eq!(29, rose.items[0].sell_in);
        assert_eq!(0, rose.items[1].quality);
        assert_eq!(-2, rose.items[1].sell_in);
    }

    #[test]
    pub fn test_aged_brie_increases_in_quality() {
        let mut rose = GildedRose::new(vec![
            Item::new("Aged Brie", 30, 10),
            Item::new("Aged Brie", -1, 10),
        ]);
        rose.update_quality();
        assert_eq!(11, rose.items[0].quality);
        assert_eq!(29, rose.items[0].sell_in);
        assert_eq!(12, rose.items[1].quality);
        assert_eq!(-2, rose.items[1].sell_in);
    }

    #[test]
    pub fn test_aged_brie_increases_up_to_limit() {
        let mut rose = GildedRose::new(vec![
            Item::new("Aged Brie", 30, 49),
            Item::new("Aged Brie", -1, 49),
        ]);
        rose.update_quality();
        assert_eq!(50, rose.items[0].quality);
        assert_eq!(29, rose.items[0].sell_in);
        assert_eq!(50, rose.items[1].quality);
        assert_eq!(-2, rose.items[1].sell_in);
    }

    #[test]
    pub fn test_backstage_passes() {
        let mut rose = GildedRose::new(vec![
            Item::new("Backstage passes to a TAFKAL80ETC concert", 30, 10),
            Item::new("Backstage passes to a TAFKAL80ETC concert", 9, 10),
            Item::new("Backstage passes to a TAFKAL80ETC concert", 5, 10),
            Item::new("Backstage passes to a TAFKAL80ETC concert", 1, 10),
            Item::new("Backstage passes to a TAFKAL80ETC concert", 0, 10),
        ]);
        rose.update_quality();
        assert_eq!(11, rose.items[0].quality);
        assert_eq!(29, rose.items[0].sell_in);
        assert_eq!(12, rose.items[1].quality);
        assert_eq!(8, rose.items[1].sell_in);
        assert_eq!(13, rose.items[2].quality);
        assert_eq!(4, rose.items[2].sell_in);
        assert_eq!(13, rose.items[3].quality);
        assert_eq!(0, rose.items[3].sell_in);
        assert_eq!(0, rose.items[4].quality);
        assert_eq!(-1, rose.items[4].sell_in);
    }

    #[test]
    pub fn test_legendary_item() {
        let mut rose = GildedRose::new(vec![Item::new("Sulfuras, Hand of Ragnaros", 30, 80)]);
        rose.update_quality();
        rose.update_quality();
        assert_eq!(80, rose.items[0].quality);
        assert_eq!(30, rose.items[0].sell_in);
    }
}
