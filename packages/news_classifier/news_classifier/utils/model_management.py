import joblib
from sklearn.pipeline import Pipeline

from news_classifier.config import paths

from news_classifier.version import __version__


def _get_latest_model_path() -> str:
    save_file_name = f"{paths.PIPELINE_SAVE_FILE}{__version__}.pkl"
    save_path = paths.MODELS_DIR / save_file_name
    return save_path


def save_pipeline(pipeline: Pipeline) -> None:
    """
    Store a pipeline
    :param pipeline: A scikit-learn pipeline
    """
    save_path = _get_latest_model_path()
    joblib.dump(pipeline, save_path)


def load_pipeline() -> Pipeline:
    """
    Load the latest pipeline
    """
    load_path = _get_latest_model_path()
    model = joblib.load(load_path)
    return model
