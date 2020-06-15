from flask import Flask, request

app = Flask(__name__)


@app.route("/")
def index():
    return "News classifier webapp"


@app.route("/classify", methods=['POST'])
def classify_news():
    if request.method == 'POST':
        article_text = request.form['text']
        return article_text
    return 'hello'


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True
    )
