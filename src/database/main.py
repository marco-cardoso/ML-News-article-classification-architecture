from pymongo import MongoClient
from database import configs as cfg

client = MongoClient(
    host=cfg.host,
    port=cfg.port
)

db = client[cfg.database]
collection = db['articles']


def insert_article(article: dict):
    return collection.insert_one(article)
