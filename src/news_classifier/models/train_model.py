from os import path

from sklearn.svm import LinearSVC
from sklearn.externals import joblib

from news_classifier.database.main import Database
from news_classifier.features.build_features import build_features


def train():
    db = Database()
    df = db.read_articles()

    X, y = build_features(
        df=df,
        transf_output_path="models",
        save_transformers=True
    )

    estimator = LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001)
    estimator.fit(X, y)

    joblib.dump(estimator, path.join("models", "model.gz"))


if __name__ == "__main__":
    train()
