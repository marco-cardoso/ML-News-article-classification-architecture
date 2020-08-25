from sklearn.compose import ColumnTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC

from news_classifier.config import variables
from news_classifier.features import DropFeatures

category_classifier = Pipeline(
    steps=[
        ("drop_features", DropFeatures(variables.DROP_FEATURES)),
        ('column_transformer', ColumnTransformer(
            transformers=[
                ('tfid', TfidfVectorizer(), variables.TEXT_FEATURES)
            ]
        )),
        ('clf', LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001))
    ]
)
