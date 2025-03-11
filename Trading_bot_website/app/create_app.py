import create_app
from flask import Flask, render_template


def create_app():
    app = Flask(__name__)

    # Import blueprint using relative import
    from .routes import api  
    app.register_blueprint(api)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
