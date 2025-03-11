from flask import Flask

def create_app():
    app = Flask(__name__)

    # Load configurations, extensions, etc.
    app.config.from_object('config.Config')

    # Import and register routes
    from .routes import api
    app.register_blueprint(api)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True) # Run the application in debug mode