"""
    Module to store the path settings
"""
import pathlib

import news_classifier

PACKAGE_ROOT = pathlib.Path(news_classifier.__file__).resolve().parent
MODELS_DIR = PACKAGE_ROOT / "models"

PIPELINE_NAME = "linear_svc"
PIPELINE_SAVE_FILE = f"{PIPELINE_NAME}_output_v"

