from flask import Blueprint

api = Blueprint('api', __name__)

@api.route('/')
def home():
    return "Welcome to the AI Trading Bot!"