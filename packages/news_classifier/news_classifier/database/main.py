import os

from pymongo import MongoClient


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

        mongo_host = os.environ.get("MONGO_HOST")
        mongo_port = int(os.environ.get("MONGO_PORT"))
        mongo_root_username = os.environ.get("MONGO_INITDB_ROOT_USERNAME")
        mongo_root_passwd = os.environ.get("MONGO_INITDB_ROOT_PASSWORD")

        mongo_url = f"mongodb://{mongo_root_username}:{mongo_root_passwd}@{mongo_host}:{mongo_port}"

        client = MongoClient(
            mongo_url,
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


db = Database()
