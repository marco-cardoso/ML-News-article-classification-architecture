import typing as t

import pandas as pd

from news_classifier.utils.model_management import load_pipeline
from news_classifier.utils import text_examples
from news_classifier.version import __version__

pipeline = load_pipeline()


def predict(input_data: t.Union[pd.DataFrame, dict]) -> dict:
    data = pd.DataFrame([input_data])

    prediction = pipeline.predict(data)
    results = {"predictions": prediction, "version": __version__}
    return results


if __name__ == "__main__":
    data = {
        'content': text_examples.business
    }
    predict(data)
