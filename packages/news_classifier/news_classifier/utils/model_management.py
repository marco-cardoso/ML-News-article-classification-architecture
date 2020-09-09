from pathlib import Path
import logging

import joblib
from sklearn.pipeline import Pipeline

from news_classifier.config import paths
from news_classifier.database import db
from news_classifier.config.s3 import bucket
from news_classifier.utils.exceptions import NoModelFoundException
from news_classifier.version import __version__

_logger = logging.getLogger(__name__)


def _create_new_model_path() -> Path:
    """
    Use the latest article date stored in the database to create
    a model path.
    :return: A string to set the path of a recently created model
    """
    latest_article_date = db.get_last_article_date()
    ad_timestamp = latest_article_date.timestamp()

    pipeline_name = paths.PIPELINE_NAME
    pipeline_version = __version__

    save_file_name = f"{ad_timestamp}.pkl"
    save_path = paths.MODELS_DIR / save_file_name
    _logger.debug("Model stored path : " + str(save_path))
    return save_path


def _get_available_local_models() -> list:
    """
    Get all models inside the path stored in paths.MODELS_DIR
    :return: A list with all models found
    """
    models = list(paths.MODELS_DIR.glob("*.pkl"))
    return models


def _get_latest_local_model_name() -> str:
    """
    Get the names of all models stored in the paths.MODELS_DIR folder,
    sort them based on their names(timestamps) and return the one with
    the highest value. The most recent.
    :return: A string with the path of the latest local model
    """
    models = _get_available_local_models()
    # Remove the extension from the filenames for comparison when sorting
    # the values
    models = map(lambda x: x.stem, models)
    # Sort the filenames
    models = list(sorted(models, reverse=True))

    if len(models) == 0:
        raise NoModelFoundException()

    # Get the model with the highest timestamp value
    latest_model_name = models[0]
    return latest_model_name


def _get_latest_local_model_path() -> Path:
    """
    Get the latest local model name and add the default extension name
    :return: The path of the latest local model
    """
    latest_model_name = _get_latest_local_model_name()
    latest_model_path = paths.MODELS_DIR / (latest_model_name + ".pkl")
    return latest_model_path


def save_pipeline(pipeline: Pipeline) -> None:
    """
    Store a pipeline locally
    :param pipeline: A scikit-learn pipeline
    """
    _logger.info("Storing the model locally")
    save_path = _create_new_model_path()
    joblib.dump(pipeline, save_path)
    _logger.info("Model successfully stored")

    bucket.upload_file(save_path)
    bucket.remove_old_models(
        keep_model=str(save_path.name)
    )


def load_pipeline() -> Pipeline:
    """
    Load the latest pipeline
    """
    _logger.info("Loading the model")
    load_path = _get_latest_local_model_path()
    model = joblib.load(load_path)
    _logger.info("Model sucessfully loaded")
    return model


def new_model_available() -> bool:
    """
    Check if there's a new model available in S3
    :return: A boolean with the result
    """
    latest_s3_model_name = bucket.get_last_model_name()

    try:
        latest_local_model = _get_latest_local_model_name()
    except NoModelFoundException:
        return True

    return latest_s3_model_name != latest_local_model


def remove_old_models(keep_model: Path):
    """
    Remove all models in the models folder but the keep_model
    :param keep_model: A Path with the latest model. This is the
    model that is not gonna be deleted.
    """
    _logger.info("Removing old models")
    models = _get_available_local_models()
    models.remove(keep_model)

    for model in models:
        model.unlink()
        _logger.info(f"{model} removed")

    _logger.info("Out of date models removed successfully")


def update_model(pipeline: Pipeline = None):
    """
    Check S3, if there's a newer model then it replaces the latest local model
    with the S3 latest model
    """
    _logger.info("Checking if there's a new ML model available")
    if new_model_available():
        _logger.info("New ML model available, updating the models folder")

        latest_s3_model_name = bucket.get_last_model_name() + ".pkl"
        output_path = paths.MODELS_DIR / latest_s3_model_name
        bucket.download_file(
            filename=str(latest_s3_model_name),
            output_path=str(output_path)
        )

        pipeline = joblib.load(output_path)

        remove_old_models(keep_model=output_path)
        _logger.info("New ML model ready to use")
    else:
        _logger.info("The model being used is the latest")

    return pipeline
