"""
Define item pipelines here.
"""
from MySQLdb import connect, Error
from imdb_scraper import database as db
import logging as log

logger = log.getLogger(__name__)


class TitlePipeline:
    """
    Pipeline for the Title scraper.
    """

    def __init__(self):
        # Set-up connection details.
        self.connection = connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='imdb_scraper'
        )
        # Create a cursor for executing commands.
        self.cursor = self.connection.cursor()
        self.setup_table()

    def setup_table(self):
        """
        Set-up table.
        """
        # Create tables if they don't exist.
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS titles(
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    genre_id INT,
                    name TEXT NOT NULL,
                    certificate TEXT,
                    runtime INT,
                    imdb_rating FLOAT,
                    page_identifier TEXT NOT NULL,
                    CONSTRAINT FK_TitlesGenres FOREIGN KEY (genre_id)
                        REFERENCES genres(id)
                )
            """)
        except Error as error:
            logger.error("Error %s: %s" % (error.args[0], error.args[1]))

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        try:
            logger.info('Checking: %s' % (item['name']))
            self.cursor.execute("""
                                        SELECT COUNT(*) FROM `titles` WHERE `name` = %s
                                    """, (
                item['name'],
            ))
            count = self.cursor.fetchone()[0]
            logger.info(
                count
            )
            if count < 1:
                logger.info('Saving: %s' % (item['name']))
                self.cursor.execute("""
                    INSERT INTO `titles` (
                        `genre_id`, `name`, `certificate`, `runtime`, `imdb_rating`, `page_identifier`
                    )
                    VALUES (%s,%s,%s,%s,%s,%s)
                """, (
                    item['genre_id'],
                    item['name'],
                    item['certificate'],
                    item['runtime'],
                    item['imdb_rating'],
                    item['page_identifier'],
                ))
                self.connection.commit()
                logger.info('Saved')
            logger.info('closed')
        except Error as error:
            logger.error("Error %s: %s" % (error.args[0], error.args[1]))
        return item


class RatingPipeline:
    """
    Pipeline for the Rating scraper.
    """

    def __init__(self):
        # Set-up connection details.
        self.conn = connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='imdb_scraper',
            port='3306'
        )
        # Create a cursor for executing commands.
        self.cursor = self.conn.cursor()
        self.setup_table()

    def setup_table(self):
        """
        Set-up table
        :return:
        """
        try:
            # Create tables if they don't exist.
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS ratings(
                            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY
                        )
                    """)
        except Error as error:
            print("Error %s: %s" % (error.args[0], error.args[1]))

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        return item


class CastPipeline:
    """
    Pipeline for the Cast scraper.
    """

    def __init__(self):
        # Set-up connection details.
        self.conn = connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='imdb_scraper',
            port='3306'
        )
        # Create a cursor for executing commands.
        self.cursor = self.conn.cursor()
        self.setup_table()

    def setup_table(self):
        """
        Set-up table.
        :return:
        """
        try:
            # Create tables if they don't exist.
            self.cursor.execute("""
                        CREATE TABLE IF NOT EXISTS cast(
                            id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                        )
                    """)
        except Error as error:
            logger.error("Error %s: %s" % (error.args[0], error.args[1]))

    def process_item(self, item, spider):
        """
        :param item:
        :param spider:
        :return:
        """
        return item


class GenrePipeline:
    """
    Pipeline for the Genres.
    """

    def __init__(self):
        # Set-up connection details.
        self.conn = connect(
            host='127.0.0.1',
            user='root',
            password='',
            database='imdb_scraper'
        )
        # Create a cursor for executing commands.
        self.cursor = self.conn.cursor()
        self.setup_table()

    def setup_table(self):
        """
        Set-up table.
        :return:
        """
        try:
            # Create tables if they don't exist.
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS genres(
                    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    name TEXT NOT NULL,
                    ordering INT NOT NULL
                )
            """)
            # Run method that inserts genres to database.
            db.insert_genres(self.conn, self.cursor)
        except Error as error:
            logger.error("Error %s: %s" % (error.args[0], error.args[1]))
