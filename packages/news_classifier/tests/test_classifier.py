from news_classifier.models.predict import predict
from news_classifier.utils import text_examples


def test_prediction():
    data = {
        'content': text_examples.business
    }
    result = predict(data)

    assert result is not None
    assert isinstance(result.get('prediction'), str)
    assert result.get("prediction") == "business"

