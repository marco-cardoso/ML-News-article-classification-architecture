from pymongo import MongoClient
from database import configs as cfg


class Database:

    def __init__(self) -> None:
        super().__init__()

        client = MongoClient(
            host=cfg.host,
            port=cfg.port,
            maxPoolSize=20
        )

        db = client[cfg.database]
        self.collection = db['articles']

    def insert_article(self, article: dict):
        return self.collection.insert_one(article)
