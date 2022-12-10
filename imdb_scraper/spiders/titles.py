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
            raise CloseSpider('Spider Closed: Error at titles.py, line 35.')

        genre_names = []
        for genre_name in self.available_genres:
            genre_names.append(genre_name[1])

        for genres in self.available_genres:
            if genre not in genre_names:
                logger.error(f'Reason: Genre {genre} is not available to crawl.')
                raise CloseSpider("Spider Closed: Error at titles.py, line 44.")
            elif genres[1] == genre:
                self.selected_genre = genres
                self.sort = sort
                break

        self.start_urls = [f'https://www.imdb.com/search/title/?genres={self.selected_genre[1]}&sort={self.sort}']

    def parse(self, response):
        """
        :param self:
        :param response:
        """
        for card in response.xpath('//div[@class="lister-item mode-advanced"]/div[@class="lister-item-content"]'):
            title = card.xpath('.//h3[@class="lister-item-header"]/a/text()').get()
            certificate = card.xpath('.//p/span[@class="certificate"]/text()').get()
            runtime_string = card.xpath('.//p/span[@class="runtime"]/text()').get()
            if runtime_string is not None:
                runtime = int(float(str(runtime_string).split(' ')[0]))
            else:
                runtime = None
            imdb_rating_string = card.xpath(
                './/div[@class="ratings-bar"]/div[@class="inline-block ratings-imdb-rating"]/@data-value'
            ).get()
            if imdb_rating_string is not None:
                imdb_rating = float(imdb_rating_string)
            else:
                imdb_rating = None
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
