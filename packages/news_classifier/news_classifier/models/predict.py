import logging
import typing as t

import pandas as pd

from news_classifier.utils import text_examples
from news_classifier.utils.model_management import load_pipeline, update_model

# It's necessary to load the model here otherwise
# at each prediction the model will be
# reloaded increasing the processing time
pipeline = load_pipeline()


def predict(input_data: t.Union[pd.DataFrame, dict]) -> dict:
    global pipeline

    _logger = logging.getLogger(__name__)

    # This method checks if there's a new model
    # available and then updates it. Otherwise, it keeps
    # the same
    pipeline = update_model(pipeline)

    _logger.info("Generating a prediction.")
    data = pd.DataFrame([input_data])

    predictions = pipeline.predict(data)
    results = {"prediction": predictions[0]}
    return results


if __name__ == "__main__":
    data = {
        'content': text_examples.business
    }
    predict(data)
