"""
    Module to store the path settings
"""
import logging
import pathlib

import news_classifier

_logger = logging.getLogger(__name__)

PACKAGE_ROOT = pathlib.Path(news_classifier.__file__).resolve().parent
MODELS_DIR = pathlib.Path("/models").absolute()

if not MODELS_DIR.exists():
    _logger.info(f"Creating {MODELS_DIR}")
    MODELS_DIR.mkdir()

MODEL_PLOTS_DIR = MODELS_DIR / "plots"

PIPELINE_NAME = "linear_svc"

