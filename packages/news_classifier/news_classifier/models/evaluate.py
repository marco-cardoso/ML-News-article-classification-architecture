import logging

import mlflow
import mlflow.sklearn
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.model_selection import KFold

from news_classifier.utils.model_management import _create_new_model_path

_logger = logging.getLogger(__name__)


def get_overall_results(results) -> dict:
    overall_results = {}

    df = pd.DataFrame.from_dict(results, orient="index")
    for metric in df.columns:
        overall_results[metric + "_mean"] = df[metric].mean()
        overall_results[metric + "_std"] = df[metric].std()

    return overall_results


def calculate_efficiency_metrics(pipeline, X, y):
    """
    Apply KFold to the given data and calculate the follow metrics for each fold :
        - accuracy
        - precision
        - recall
        - f1-score
        - confusion matrix

    Finally, it will calculate for each metric its mean and standard deviation.
    :param pipeline: A Sklearn pipeline
    :param X: A numpy array with the features
    :param y: A numpy array with the target
    """
    _logger.info("Calculating efficiency metrics")

    with mlflow.start_run():

        model_timestamp = str(_create_new_model_path().name)
        mlflow.set_tag("model_version", model_timestamp)

        kfold = KFold(n_splits=5, random_state=4532, shuffle=True)
        results = {}

        fold_number = 0
        for train_index, test_index in kfold.split(X):
            X_train, X_test = X.iloc[train_index], X.iloc[test_index]
            y_train, y_test = y.iloc[train_index], y.iloc[test_index]

            pipeline.fit(X_train, y_train)

            y_pred = pipeline.predict(X_test)

            metrics = {
                'accuracy': accuracy_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, average="weighted", labels=np.unique(y_pred)),
                'recall': recall_score(y_test, y_pred, average="weighted", labels=np.unique(y_pred)),
                'f1': f1_score(y_test, y_pred, average="weighted", labels=np.unique(y_pred))
            }

            results[fold_number] = metrics
            fold_number += 1

        overall_results = get_overall_results(results)
        mlflow.log_metrics(overall_results)

    _logger.info("Metrics generated successfully")
