import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve


def plot(estimator, X: np.array, y: np.array, title: str) -> np.array:
    """
    It generates and displays the learning curve for the given estimator and data.
    :param estimator: A scikit-learn estimator
    :param X: A Pandas dataframe with the X values
    :param y: An array with the y values
    :param title: A string with the name of the estimator
    :return: The learning curve results
    """
    lc_results = learning_curve(estimator, X, y, cv=5, n_jobs=-1, random_state=123)

    xlabel = lc_results[0]

    mean_train_scores = np.array([np.mean(scores) for scores in lc_results[1]])
    mean_test_scores = np.array([np.mean(scores) for scores in lc_results[2]])

    std_train_scores = np.array([np.std(scores) for scores in lc_results[1]])
    std_test_scores = np.array([np.std(scores) for scores in lc_results[2]])

    fig, ax = plt.subplots(1, 1, figsize=(10, 5))

    sns.lineplot(x=xlabel, y=mean_train_scores, ax=ax, label="Train scores")
    sns.lineplot(x=xlabel, y=mean_test_scores, ax=ax, label="Test scores")

    ax.grid()
    ax.fill_between(xlabel, mean_train_scores - std_train_scores,
                    mean_train_scores + std_train_scores, alpha=0.1)
    ax.fill_between(xlabel, mean_test_scores - std_test_scores,
                    mean_test_scores + std_test_scores, alpha=0.1)

    plt.title(f"{title} Learning Curve")
    plt.xlabel("Amount of used observations")
    plt.ylabel("Accuracy score")

    plt.show()
    return lc_results
