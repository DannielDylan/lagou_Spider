# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.conf import settings


class LagouWebsitePipeline(object):
    def process_item(self, item, spider):
        return item


class MongoDBPipeline(object):
    def __init__(self):
        self.server = settings['MONGODB_SERVER']
        self.port = settings['MONGODB_PORT']
        self.db = settings['MONGODB_DB']
        self.col = settings['MONGODB_COLLECTION']

    # @classmethod
    # def from_crawler(cls,crawler):
    #     return cls(
    #         mongo_server="mongodb://localhost:27017",
    #         mongo_db='lagou'
    #     )
    def open_spider(self, spider):
        self.mongo_client = pymongo.MongoClient(self.server, self.port)
        db = self.mongo_client[self.db]
        self.collection = db[self.col]

    def process_item(self, item, spider):

        result = self.collection.find_one(
                {'companyFullName': item['companyFullName']}
        )
        if result:
            pass
        else:
            self.collection.insert(dict(item))

        return item

    def close_spider(self, spider):
        self.mongo_client.close()
