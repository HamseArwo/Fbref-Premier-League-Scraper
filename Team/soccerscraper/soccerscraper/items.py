# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SoccerscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ClubItems(scrapy.Item):
    team = scrapy.Field()
    rank = scrapy.Field()
    match_played = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    points = scrapy.Field()
    goal_differences = scrapy.Field()
    top_scorer = scrapy.Field()
    image = scrapy.Field()
