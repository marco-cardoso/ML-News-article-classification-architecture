import numpy as np

from flask import Flask, request

from news_classifier.models import predict


app = Flask(__name__)


@app.route("/")
def index():
    return "News classifier webapp"


@app.route("/classify", methods=['POST'])
def classify_news():
    if request.method == 'POST':
        article_text = request.form['text']
        category = predict(np.array(
            [
                article_text
            ]
        ))
        return category[0]


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True
    )
