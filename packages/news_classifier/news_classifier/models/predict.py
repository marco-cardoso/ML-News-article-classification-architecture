import typing as t
import logging

import pandas as pd

from news_classifier.utils.model_management import load_pipeline
from news_classifier.utils import text_examples
from news_classifier.version import __version__

pipeline = load_pipeline()


def predict(input_data: t.Union[pd.DataFrame, dict]) -> dict:
    _logger = logging.getLogger(__name__)

    _logger.info("Generating a prediction.")
    data = pd.DataFrame([input_data])

    predictions = pipeline.predict(data)
    results = {"prediction": predictions[0], "version": __version__}
    return results


if __name__ == "__main__":
    data = {
        'content': text_examples.business
    }
    predict(data)
