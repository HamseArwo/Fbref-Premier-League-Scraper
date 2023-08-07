# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from playerscraper.items import PlayerItem, GkItem
import pymongo
from pymongo import MongoClient


class PlayerscraperPipeline:
    def process_item(self, item, spider):
        return item


class PlayerPipeline:
    def __init__(self):
        self.connection = MongoClient("mongodb://localhost:27017/")
        self.dataBase = self.connection["Premier_League"]
        self.collection = self.dataBase["Players"]

    def process_item(self, item, spider):
        if isinstance(item, PlayerItem):
            adapter = ItemAdapter(item)
            for x in adapter:
                if adapter[x] == None:
                    adapter[x] = 0

            adapter["goals"] = int(adapter["goals"])
            adapter["assist"] = int(adapter["assist"])

            # export = self.collection.insert_one(dict(item))

        return item


class GkPipeline:
    def __init__(self):
        self.connection = MongoClient("mongodb://localhost:27017/")
        self.dataBase = self.connection["Premier_League"]
        self.collection = self.dataBase["Gk"]

    def process_item(self, item, spider):
        if isinstance(item, GkItem):
            adapter = ItemAdapter(item)
            for x in adapter:
                if adapter[x] == None:
                    adapter[x] = "0"
            adapter["saves_percent"] = float(adapter["saves_percent"])
            adapter["clean_sheets"] = int(adapter["clean_sheets"])

            export = self.collection.insert_one(dict(item))

        return item
