import pandas as pd

from news_classifier.database import db


def load_data(projection: dict) -> pd.DataFrame:
    """
    Load the data from the Mongo collection and transform
    into a pandas dataframe
    :projection: A dictionary with the fields to load from database
    :return: A pandas dataframe with the data
    """
    articles = db.read_articles(
        projection=projection
    )
    return pd.DataFrame(articles)
