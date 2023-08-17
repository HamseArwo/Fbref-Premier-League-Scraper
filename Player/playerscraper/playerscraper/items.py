# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GkItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    club = scrapy.Field()
    apperances = scrapy.Field()
    age = scrapy.Field()
    national_team = scrapy.Field()
    mins_played = scrapy.Field()
    ga = scrapy.Field()
    ga_per_90 = scrapy.Field()
    SoTA = scrapy.Field()
    saves = scrapy.Field()
    saves_percent = scrapy.Field()
    clean_sheets = scrapy.Field()
    image = scrapy.Field()
    year = scrapy.Field()


class PlayerItem(scrapy.Item):
    name = scrapy.Field()
    position = scrapy.Field()
    club = scrapy.Field()
    apperances = scrapy.Field()
    age = scrapy.Field()
    national_team = scrapy.Field()
    mins_played = scrapy.Field()
    goals = scrapy.Field()
    assist = scrapy.Field()
    ga = scrapy.Field()
    npg = scrapy.Field()
    pkg = scrapy.Field()
    xg = scrapy.Field()
    xast = scrapy.Field()
    image = scrapy.Field()
    year = scrapy.Field()
