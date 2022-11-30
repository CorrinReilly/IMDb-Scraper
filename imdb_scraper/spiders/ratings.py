"""
Spider for scraping the ratings of a title.
"""
import scrapy


class RatingsSpider(scrapy.Spider):
    """
    Define class RatingsSpider
    :param scrapy.Spider
    """
    name = 'ratings'
    allowed_domains = ['www.imdb.com']
    start_urls = ['http://www.imdb.com/']

    def parse(self, response):
        """
        :param response:
        """
        pass
