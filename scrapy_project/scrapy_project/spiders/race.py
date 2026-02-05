import scrapy


class RaceSpider(scrapy.Spider):
    name = "race"
    allowed_domains = ["sansilvestrecoruna.com"]
    start_urls = ["https://sansilvestrecoruna.com/"]

    def parse(self, response):
        pass
