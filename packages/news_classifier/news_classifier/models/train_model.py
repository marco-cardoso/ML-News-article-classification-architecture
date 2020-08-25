from news_classifier.news_classifier.config import variables
from news_classifier.news_classifier.models import category_classifier
from news_classifier.news_classifier.utils import load_data, model_management


def train():
    df = load_data()
    X, y = df[variables.FEATURES]

    category_classifier.fit(X, y)
    model_management.save_pipeline(category_classifier)


if __name__ == "__main__":
    train()
