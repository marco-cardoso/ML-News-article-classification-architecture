from os import path

from news_classifier.features.build_features import build_features_ml
from sklearn.externals import joblib
from sklearn.svm import LinearSVC


def train():
    X, y, le = build_features_ml(
        transf_output_path="models",
        save_transformers=True
    )

    estimator = LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001)
    estimator.fit(X, y)

    joblib.dump(estimator, path.join("models", "model.gz"))


if __name__ == "__main__":
    train()
