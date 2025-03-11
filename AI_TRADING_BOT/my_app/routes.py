from flask import Blueprint, render_template

# Create a Blueprint
main_bp = Blueprint('main', __name__)

# Define routes
@main_bp.route('/')
def home():
    return render_template('index.html')  # Render the welcome page