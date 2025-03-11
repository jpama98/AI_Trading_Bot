from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configurations
    app.config.from_object('config.Config')

    # Register routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app  # Return the Flask app instance