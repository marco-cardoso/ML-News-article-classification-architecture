from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import LinearSVC

from news_classifier.config import variables

category_classifier = Pipeline([
    ColumnTransformer(
        [
            ('tfid_vec', TfidfVectorizer(stop_words="english"), variables.TEXT_FEATURES),
            ('le', LabelEncoder(), variables.TARGET)
        ]
    ),
    ('clf',  LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001))
])
