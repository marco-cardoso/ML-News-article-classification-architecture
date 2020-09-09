import os
import datetime
import logging

from pymongo import MongoClient

_logger = logging.getLogger(__name__)


class Database:
    """
    It's a wrapper for the PyMongo Client with a couple of necessary
    operations
    """

    def __init__(self) -> None:
        """
        It starts the PyMongo client and loads the articles collection
        reference
        """
        _logger.info("Initiating the database module !")
        super().__init__()

        mongo_host = os.environ.get("MONGO_HOST")
        mongo_port = int(os.environ.get("MONGO_PORT"))
        mongo_root_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
        mongo_root_passwd = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")

        if (mongo_root_username is not None) and (mongo_root_passwd is not None):
            mongo_url = f"mongodb://{mongo_root_username}:{mongo_root_passwd}@{mongo_host}:{mongo_port}"
        else:
            mongo_url = f"mongodb://{mongo_host}:{mongo_port}"

        client = MongoClient(
            mongo_url,
            maxPoolSize=20
        )

        db = client["news-classifier"]
        self.collection = db['articles']
        self.predictions = db['predictions']
        _logger.info("Database module successfully loaded.")

    def insert_article(self, article: dict):
        """
        It inserts an article into the database
        :param article: A Dictionary with the article data
        """
        return self.collection.insert_one(article)

    def insert_prediction(self, prediction: dict):
        """
        It inserts a prediction output into the database
        :param prediction: A Dictionary with the prediction
        """
        return self.predictions.insert_one(prediction)

    def read_articles(self, projection: dict = None) -> list:
        """
        It reads all the articles in the database
        :return: A list with the news articles
        """
        if projection is None:
            projection = {
                '_id': False
            }

        articles = list(self.collection.find(
            filter={},
            projection=projection
        ))
        return articles

    def get_last_article_date(self) -> datetime.datetime:
        """
        It returns the newest article date
        """
        last_article_cusor = self.collection.find(
            filter={},
            projection={
                '_id': False,
                'published_on': True
            }
        ).sort(
            [
                ('published_on', -1)
            ]
        ).limit(1)

        if last_article_cusor.count() != 0:
            return last_article_cusor[0]['published_on']

        print("Database with no articles ! ")


db = Database()
