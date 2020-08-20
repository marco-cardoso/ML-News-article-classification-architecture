import os

from pymongo import MongoClient
import pandas as pd


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
        super().__init__()

        client = MongoClient(
            host=os.environ.get("MONGO_HOST"),
            port=os.environ.get("MONGO_PORT"),
            maxPoolSize=20
        )

        db = client["news-classifier"]
        self.collection = db['articles']

    def insert_article(self, article: dict):
        """
        It inserts an article into the database
        :param article: A Dictionary with the article data
        """
        return self.collection.insert_one(article)

    def read_articles(self, projection: dict = None) -> pd.DataFrame:
        """
        It reads all the articles from the database and converts them into
        a pandas dataframe
        :return: A pandas DataFrame
        """
        if projection is None:
            projection = {
                '_id': False
            }

        articles = list(self.collection.find(
            filter={},
            projection=projection
        ))
        return pd.DataFrame(articles)
