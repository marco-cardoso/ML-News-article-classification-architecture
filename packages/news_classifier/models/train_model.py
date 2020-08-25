from news_classifier.config import variables
from news_classifier.database import db
from news_classifier.models import pipeline
from news_classifier.utils import load_data

def train():
    df = db.read_articles()
    X, y = df[variables.FEATURES]

    pipeline.category_classifier.fit(X, y)


if __name__ == "__main__":
    train()
