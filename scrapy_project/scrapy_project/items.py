# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyProjectItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    fecha = scrapy.Field()
    runner_name = scrapy.Field()
    finish_time = scrapy.Field()
    age_group = scrapy.Field()
    gender = scrapy.Field()
    race_distance = scrapy.Field()
    location = scrapy.Field()
