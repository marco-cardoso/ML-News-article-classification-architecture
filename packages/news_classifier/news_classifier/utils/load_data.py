import pandas as pd

from news_classifier.news_classifier.database import db


def load_data() -> pd.DataFrame:
    """
    Load the data from the Mongo collection and transform
    into a pandas dataframe
    :return: A pandas dataframe with the data
    """
    articles = db.read_articles()
    return pd.DataFrame(articles)

