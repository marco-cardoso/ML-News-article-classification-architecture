from os import path

import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.externals import joblib

import nltk

from news_classifier.database.main import Database

nltk.download('stopwords')
nltk.download('wordnet')
STOPWORDS = nltk.corpus.stopwords.words('english')

tokenizer = nltk.RegexpTokenizer(r'\w+')
lemmatizer = nltk.stem.WordNetLemmatizer()


def build_features_ml(
        transf_output_path: str = None,
        save_transformers: bool = False) -> tuple:
    """
    It builds the features to feed a ML model
    :param save_transformers: A boolean representing the wish to save the
    used transformer or not
    :param transf_output_path: A string with the output path of the
    transformers to be saved
    :return: A tuple with X and Y data
    """
    db = Database()
    df = db.read_articles()

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

    return X, y, le


def build_features_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """
     It builds the features to perform data analysis for a given dataframe
    :param df: A Pandas dataframe with the articles
    :return: A Pandas dataframe with the new features
    """
    text_columns = ['content', 'title']

    for column in text_columns:
        # Changing to lower case and removing punctuation
        df[column] = df[column].apply([lambda column: column.str.lower().str.replace('[^\w\s]', '')], axis=0)

        # Tokenizing the corpus
        df[column] = df[column].apply(lambda x: tokenizer.tokenize(x))

        # Removing stopwords from corpus
        df[column] = df[column].apply(lambda x: [item for item in x if item not in STOPWORDS])

        # Lemmatizing the corpus
        df[column] = df[column].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

    df['topics'] = df['topics'].apply(preprocess_topics)

    df['cnt_char_amt'] = df['content'].apply(len)
    df['title_char_amt'] = df['title'].apply(len)

    return df


def preprocess_topics(topics):
    topics = [lemmatizer.lemmatize(item.lower()) for item in topics if item not in STOPWORDS]
    return topics


def read_analysis_df():
    db = Database()
    df = db.read_articles()
    return build_features_analysis(df)

