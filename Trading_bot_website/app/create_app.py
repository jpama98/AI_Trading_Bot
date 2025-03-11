from flask import Flask, render_template

def create_app():
    app = Flask(__name__)

    from app.routes import api
    app.register_blueprint(api)

    @app.route("/")
    def home():
        return render_template("index.html")

    return app
# # # Compare this snippet from Trading_bot_website/app/routes.py:
# # import requests