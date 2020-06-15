from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer


def train():
    estimator = LinearSVC(C=0.5, dual=True, loss='squared_hinge', penalty='l2', tol=0.001)
