import numpy as np

from flask import Flask, request, render_template, redirect, session

from news_classifier.models import predict, text_examples


app = Flask(__name__)
app.secret_key = "}@$/=(+@;7`9~8/5"


@app.route("/")
def index():

    if 'news-article' not in session:
        session['news-article'] = text_examples.business

    return render_template("index.html")


@app.route("/classify", methods=['POST'])
def classify_news():
    if request.method == 'POST':
        article_text = request.form['text']

        session['news-article'] = article_text

        category = predict(np.array(
            [
                article_text
            ]
        ))[0]

        session['category'] = category
        return redirect("/")


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True
    )
