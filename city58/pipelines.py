# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exporters import CsvItemExporter
from city58.items import Community, SecondHandHouse, Rental

class City58CsvPipeline:

    def open_spider(self, spider):
        self.community_file = open('community.csv', 'wb')
        self.shh_file = open('shh.csv', 'wb')
        self.rental_file = open('rental.csv', 'wb')
        self.c_expr = CsvItemExporter(self.community_file)
        self.s_expr = CsvItemExporter(self.shh_file)
        self.r_expr = CsvItemExporter(self.rental_file)
        self.c_expr.start_exporting()
        self.s_expr.start_exporting()
        self.r_expr.start_exporting()

    def process_item(self, item, spider):
        if isinstance(item, Community):
            self.c_expr.export_item(item)
        elif isinstance(item, SecondHandHouse):
            self.s_expr.export_item(item)
        else:
            self.r_expr.export_item(item)
        return item

    def close_spider(self, spider):
        self.c_expr.finish_exporting()
        self.s_expr.finish_exporting()
        self.r_expr.finish_exporting()
        self.community_file.close()
        self.shh_file.close()
        self.rental_file.close()
