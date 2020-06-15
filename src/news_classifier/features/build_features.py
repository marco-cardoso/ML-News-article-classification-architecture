from os import path

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib


def build_features(
        df: pd.DataFrame,
        transf_output_path: str,
        save_transformers: bool = False) -> tuple:
    """
    It builds the features for a given dataset
    :param df: A Pandas dataframe with the features to be transformed
    :param save_transformers: A boolean representing the wish to save the
    used transformer or not
    :param transf_output_path: A string with the output path of the
    transformers to be saved
    :return: A tuple with X and Y data
    """
    X, y = df['content'], df['category']

    tfid = TfidfVectorizer(
        stop_words="english"
    )

    le = LabelEncoder()

    X = tfid.fit_transform(X)
    y = le.fit_transform(y)

    if save_transformers:
        joblib.dump(
            tfid,
            filename=path.join(transf_output_path, "tfid.gz")
        )

        joblib.dump(
            le,
            filename=path.join(transf_output_path, "le.gz")
        )

    return X, y