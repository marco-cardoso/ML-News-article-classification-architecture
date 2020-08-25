import numpy as np

from flask import Flask, request, render_template, redirect, session

from news_classifier.models import predict, text_examples


app = Flask(__name__)
app.secret_key = "}@$/=(+@;7`9~8/5"


@app.route("/")
def index():

    # This is useful because otherwise nothing would be
    # displayed for the user to classify
    if 'news-article' not in session:
        session['news-article'] = text_examples.business

    return render_template("index.html")


@app.route("/classify", methods=['POST'])
def classify_news():
    if request.method == 'POST':
        article_text = request.form['text']

        # For some reason flask is inserting some whitespace at the beginning of
        # the text. To remove it we can use the strip function.
        article_text = article_text.strip()

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
