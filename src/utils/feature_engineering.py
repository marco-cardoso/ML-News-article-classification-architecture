import pandas as pd

import nltk

nltk.download('stopwords')
nltk.download('wordnet')
STOPWORDS = nltk.corpus.stopwords.words('english')


def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    text_columns = ['content', 'title']
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    lemmatizer = nltk.stem.WordNetLemmatizer()

    for column in text_columns:
        # Changing to lower case and removing punctuation
        df[column] = df[column].apply([lambda column: column.str.lower().str.replace('[^\w\s]', '')], axis=0)

        # Tokenizing the corpus
        df[column] = df[column].apply(lambda x: tokenizer.tokenize(x))

        # Removing stopwords from corpus
        df[column] = df[column].apply(lambda x: [item for item in x if item not in STOPWORDS])

        # Lemmatizing the corpus
        df[column] = df[column].apply(lambda x: [lemmatizer.lemmatize(word) for word in x])

    return df
