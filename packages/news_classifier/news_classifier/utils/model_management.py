import joblib
from sklearn.pipeline import Pipeline

from news_classifier.config import paths

from news_classifier.version import __version__


def save_pipeline(pipeline: Pipeline) -> None:
    """
    Store a pipeline
    :param pipeline: A scikit-learn pipeline
    """
    save_file_name = f"{paths.PIPELINE_SAVE_FILE}{__version__}.pkl"
    save_path = paths.MODELS_DIR / save_file_name

    joblib.dump(pipeline, save_path)
