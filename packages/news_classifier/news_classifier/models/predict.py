import logging
from datetime import datetime
import typing as t

import pandas as pd

from news_classifier.utils import text_examples
from news_classifier.utils.exceptions import NoModelFoundException
from news_classifier.utils.model_management import load_pipeline, update_model
from news_classifier.version import __version__
from news_classifier.database import db

_logger = logging.getLogger(__name__)

# It's necessary to load the model here otherwise
# at each prediction the model will be
# reloaded increasing the processing time
try:
    pipeline = load_pipeline()
except NoModelFoundException as e:
    _logger.info("There's not any model available")
    pipeline = update_model()


def predict(input_data: t.Union[pd.DataFrame, dict]) -> dict:
    global pipeline

    _logger = logging.getLogger(__name__)

    # This method checks if there's a new model
    # available and then updates it. Otherwise, it keeps
    # the same
    pipeline = update_model(pipeline)

    _logger.info("Generating the prediction.")
    data = pd.DataFrame([input_data])

    predictions = pipeline.predict(data)
    prediction = {
        "prediction": predictions[0],
        'datetime': datetime.utcnow(),
        'version': __version__
    }

    # Save prediction result
    log = dict(prediction)
    log['input'] = input_data
    db.insert_prediction(prediction=log)

    return prediction


if __name__ == "__main__":
    data = {
        'content': text_examples.business
    }
    predict(data)
