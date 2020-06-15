import pandas as pd

import nltk

nltk.download('stopwords')
nltk.download('wordnet')
STOPWORDS = nltk.corpus.stopwords.words('english')

tokenizer = nltk.RegexpTokenizer(r'\w+')
lemmatizer = nltk.stem.WordNetLemmatizer()

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
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
    return df

def preprocess_topics(topics):
    topics = [ lemmatizer.lemmatize(item.lower()) for item in topics if item not in STOPWORDS]
    return topics