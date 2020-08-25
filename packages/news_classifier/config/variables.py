"""
    Module to store the variable settings
"""
import pathlib
import news_classifier

PACKAGE_ROOT = pathlib.Path(news_classifier.__file__).resolve().parent

TARGET = "category"

FEATURES = [
    "category",
    "title",
    "content",
    "topics",
    "published_on"
]

# These features are only used in the data analysis process
DROP_FEATURES = ["title", "topics", "published_on"]

PIPELINE_NAME = "linear_svc"
PIPELINE_SAVE_FILE = f"{PIPELINE_NAME}_output_v"

