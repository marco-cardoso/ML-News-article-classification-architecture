import os
import logging

from news_classifier.config import variables, paths
from news_classifier.models.pipeline import category_classifier
from news_classifier.utils import load_data, model_management
from news_classifier.models.evaluate import calculate_efficiency_metrics

import mlflow

_logger = logging.getLogger(__name__)

mlflow.set_tracking_uri(f"http://{os.environ['MLFLOW_HOST']}:{os.environ['MLFLOW_PORT']}")
mlflow.set_experiment(paths.PIPELINE_NAME)


def get_features_to_use():
    features = []
    features.extend(variables.TEXT_FEATURES)
    features.extend(variables.TARGET)

    projection = {ft: True for ft in features}
    projection['_id'] = False
    return projection


def train():
    _logger.info("Loading the data from the database.")
    df = load_data(
        projection=get_features_to_use()
    )

    _logger.info("Removing duplicated values")
    df = df.drop_duplicates()

    X, y = df.loc[:, variables.TEXT_FEATURES], df[variables.TARGET]

    calculate_efficiency_metrics(category_classifier, X, y)

    _logger.info("Training the model")
    category_classifier.fit(X, y)

    _logger.info("Storing the model")
    model_management.save_pipeline(category_classifier)

    _logger.info("Model trained and stored")


if __name__ == "__main__":
    train()
