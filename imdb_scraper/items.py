"""
Define the models for scrapped items
"""
import scrapy


class TitleItem(scrapy.Item):
    """
    Model for a title
    """
    genre_id = scrapy.Field()
    name = scrapy.Field()
    certificate = scrapy.Field()
    runtime = scrapy.Field()
    imdb_rating = scrapy.Field()
    page_identifier = scrapy.Field()


class CastItem(scrapy.Item):
    """
    Model for a Cast member
    """
    pass


class RatingsItem(scrapy.Item):
    """
    Model for ratings info
    """
    pass


class GenreItem(scrapy.Item):
    """
    Model for genre types
    """
    name = scrapy.Field()
