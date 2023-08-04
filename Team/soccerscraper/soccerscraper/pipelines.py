# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from pymongo import MongoClient


class SoccerscraperPipeline:
    def __init__(self):
        self.connection = MongoClient("mongodb://localhost:27017/")
        self.dataBase = self.connection["Premier_League"]
        self.collection = self.dataBase["Teams"]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        adapter.pop("_id", None)

        export = self.collection.insert_one(dict(item))

        return item
