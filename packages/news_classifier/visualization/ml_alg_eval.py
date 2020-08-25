from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from news_classifier.visualization import confusion_matrix, learning_curve


def plot(estimator, est_name, X, y, classes):
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=123)

    estimator.fit(X_train, y_train)
    predictions = estimator.predict(X_test)

    print(f"{est_name} classification report")
    print(classification_report(y_test, predictions))

    confusion_matrix.plot(y_test, predictions, classes, classes, est_name)

    learning_curve.plot(estimator, X, y, est_name)
