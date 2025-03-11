import sys
import os
from flask import Flask, render_template

# Ensure the Trading_bot_website directory is in the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'Trading_bot_website')))

# Import Flask app properly
try:
    from Trading_bot_website.app import create_app  # Ensure correct import
except ImportError:
    print("⚠️ Module 'app.create_app' not found! Check your folder structure.")
    sys.exit(1)

# Initialize Flask app
app = create_app()

# Define a simple route to serve index.html
@app.route('/')
def home():
    return render_template('index.html')  # Ensure this file exists inside `templates/`

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
