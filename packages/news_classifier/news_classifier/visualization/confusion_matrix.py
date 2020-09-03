import logging
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix

from news_classifier.config import paths

_logger = logging.getLogger(__name__)


def plot(y_true, y_pred, xticklabels: list, yticklabels: list, title: str, to_save: bool):
    """
    It plots a confusion matrix using the seaborn heatmap function
    :param y_true: A List with the Y values
    :param y_pred: A List with the predictions
    :param xticklabels: A list with the xticklabels values
    :param yticklabels: A list with the yticklabels values
    :param title: A String with the estimator title
    :param to_save: A boolean to save the plot on disk
    :return: If the parameter save equals to true then it saves the plot
    on disk and returns its path
    """
    cm = confusion_matrix(y_true, y_pred)

    if to_save:
        fig, ax = plt.subplots(figsize=(4, 4))
    else:
        fig, ax = plt.subplots(figsize=(10, 10))

    sns.heatmap(
        cm,
        annot=True,
        xticklabels=xticklabels,
        yticklabels=yticklabels,
        fmt='g'
    )
    plt.xlabel("Predicted")
    plt.ylabel("Real")
    plt.title(f"{title} confusion matrix")

    if not to_save:
        plt.show()
    else:
        _logger.info(f"Storing {title} on disk")
        path = paths.MODEL_PLOTS_DIR / (title + ".jpg")
        plt.savefig(path)
        return path
