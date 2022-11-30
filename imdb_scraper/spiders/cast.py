"""
Spider for scraping the cast of a title.
"""
import logging
import scrapy


logger = logging.getLogger(__name__)


class CastSpider(scrapy.Spider):
    """
    Define class CastSpider
    :param scrapy.Spider
    """
    name = 'cast'
    allowed_domains = ['www.imdb.com']

    def __init__(self, **kwargs):
        """
        Set the genre and sort order of the search to crawl. If none is set default to sci-fi and popularity.
        :param genre:
        :param sort:
        :param kwargs:
        """
        super().__init__(**kwargs)
        if genre in self.available_genres:
            self.genre = genre
            self.sort = sort
            self.start_urls = [f'https://www.imdb.com/title/{title_page}/fullcredits']
        else:
            logger.info(f'Reason: Genre {genre} is not available to crawl.')

    def parse(self, response):
        """
        :param response:
        """
        pass
