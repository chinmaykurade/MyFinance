# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import pymongo
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

class MongoDBPipeline:

    collection_name = "stocks_data"

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'DEF_DB')
        )

    def open_spider(self, spider):             ## Called when spider opens
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):             ## Called when spider finishes scraping
        self.client.close()

    def process_item(self, item, spider):     ## Called for each item scraped
        self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item


class MyPDFPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.url.split("/")[-1]
        year = file_name.split('.')[0][-2:]
        extension = '.' + file_name.split('.')[-1]
        company_name = item['name']
        return company_name + year + extension