from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    # Import Blueprint using a relative import (AFTER app is initialized)
    from .routes import api  
    app.register_blueprint(api)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app

