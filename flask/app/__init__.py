

from flask import Flask, Blueprint
from dotenv import load_dotenv
from app.routes import routes
import os


def create_app():
    # Create an instance of the Flask application
    app = Flask(__name__)
    # Load environment variables from .env file
    load_dotenv()
    # Get the secret key from the environment variables
    app.secret_key = os.getenv('APP_SECRET')

    # Register the routes blueprint
    app.register_blueprint(routes)

    return app