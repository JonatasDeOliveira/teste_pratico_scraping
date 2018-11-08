# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ProductItem(scrapy.Item):
    url = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    category = scrapy.Field()
    brand = scrapy.Field()
    navigation = scrapy.Field()
    seller_name = scrapy.Field()
    price = scrapy.Field()
    old_price = scrapy.Field()
    main_image = scrapy.Field()
    sec_images = scrapy.Field()
    features = scrapy.Field()
    dimensions = scrapy.Field()
