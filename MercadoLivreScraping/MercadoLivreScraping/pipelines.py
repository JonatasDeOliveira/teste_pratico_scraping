# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json


class MercadolivrePipeline(object):
    def __init__(self):
        self.data = []

    def process_item(self, item, spider):
        self.data.append(dict(item))
        return item
        
    def open_spider(self, spider):
        #print("opeeeeeeeeeeeeeeeeeeeeeeeeen")
        try:
            with open('MercadoLivreScraping/data/data.json') as f:
                self.data = json.load(f)
        except IOError:
            pass

    def close_spider(self, spider):
        #print("closeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeed")
        with open('MercadoLivreScraping/data/data.json', 'w') as outfile:
            json.dump(self.data, outfile)
