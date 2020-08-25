from flask import Flask
from webapp.controller import app


def get_app(config) -> Flask:
    flask_app = Flask(__name__)
    flask_app.config.from_object(config)

    flask_app.register_blueprint(app)
    return flask_app


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        debug=True
    )
