from news_classifier.config import variables
from news_classifier.models.pipeline import category_classifier
from news_classifier.utils import load_data, model_management


def train():
    df = load_data()
    X, y = df[variables.FEATURES], df[variables.TARGET]

    category_classifier.fit(X, y)

    model_management.save_pipeline(category_classifier)


if __name__ == "__main__":
    train()
