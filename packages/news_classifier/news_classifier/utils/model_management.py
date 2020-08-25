import joblib
from sklearn.pipeline import Pipeline

from news_classifier.news_classifier.config import paths


def save_pipeline(pipeline : Pipeline) -> None:
    """
    Store a pipeline
    :param pipeline: A scikit-learn pipeline
    """
    save_file_name = f"{paths.PIPELINE_SAVE_FILE}.pkl"
    save_path = paths.MODELS_DIR / save_file_name

    joblib.dump(pipeline, save_path)
