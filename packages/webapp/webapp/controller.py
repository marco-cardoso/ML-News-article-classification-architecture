from flask import Blueprint, request, render_template, redirect, session

from news_classifier.utils import text_examples
from news_classifier.models.predict import predict

app = Blueprint('news_classifier_app', __name__)


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
        category = predict({'content' : article_text})['prediction']

        session['category'] = category
        return redirect("/")
