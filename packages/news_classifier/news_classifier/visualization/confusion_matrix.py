import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix


def plot(y_true, y_pred, xticklabels: list, yticklabels: list, title: str):
    """
    It plots a confusion matrix using the seaborn heatmap function
    :param y_true: A List with the Y values
    :param y_pred: A List with the predictions
    :param xticklabels: A list with the xticklabels values
    :param yticklabels: A list with the yticklabels values
    :param title: A String with the estimator title
    """
    cm = confusion_matrix(y_true, y_pred)

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

    plt.show()
