"""
Spider for scraping titles.
"""
from scrapy.exceptions import CloseSpider
from imdb_scraper import database as db
import logging as log
import scrapy
from imdb_scraper.items import TitleItem

logger = log.getLogger(__name__)


class TitleSpider(scrapy.Spider):
    """
    Define class TitleSpider
    :param scrapy.Spider
    """
    # Variables
    name = 'titles'
    allowed_domains = ['www.imdb.com']
    selected_genre = list()

    def __init__(self, genre='sci-fi', sort='popularity', **kwargs):
        """
        Set the genre and sort order of the search to crawl. If none is set default to sci-fi and popularity.
        :param genre:
        :param sort:
        :param kwargs:
        """
        super().__init__(**kwargs)
        try:
            self.available_genres = db.get_genres()
        except Exception as exception:
            logger.error("Error %s: %s" % (exception.args[0], exception.args[1]))
            CloseSpider()

        genre_names = []
        for genre_name in self.available_genres:
            genre_names.append(genre_name[1])

        for genres in self.available_genres:
            if genres[1] == genre and genre in genre_names:
                self.selected_genre = genres
                print(self.selected_genre)
                self.sort = sort
            else:
                logger.error(f'Reason: Genre {genre} is not available to crawl.')
                CloseSpider()

        self.start_urls = [f'https://www.imdb.com/search/title/?genres={self.selected_genre[1]}&sort={self.sort}']

    def parse(self, response):
        """
        :param self:
        :param response:
        """
        for card in response.xpath('//div[@class="lister-item mode-advanced"]/div[@class="lister-item-content"]'):
            title = card.xpath('.//h3[@class="lister-item-header"]/a/text()').get()
            certificate = card.xpath('.//p/span[@class="certificate"]/text()').get()
            runtime = card.xpath('.//p/span[@class="runtime"]/text()').get()
            imdb_rating = card.xpath(
                './/div[@class="ratings-bar"]/div[@class="inline-block ratings-imdb-rating"]/@data-value'
            ).get()
            title_link = card.xpath('.//h3[@class="lister-item-header"]/a/@href').get()
            page_identifier = title_link.split('/')[2]
            genre_id = self.selected_genre[0]

            item = TitleItem()
            item["genre_id"] = int(genre_id)
            item["name"] = title
            item["certificate"] = certificate
            item["runtime"] = runtime
            item["imdb_rating"] = imdb_rating
            item["page_identifier"] = page_identifier

            try:
                yield item
            except Exception as exception:
                logger.error("Error %s: %s" % (exception.args[0], exception.args[1]))
