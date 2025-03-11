import sys
import os
from flask import Flask, render_template

# Ensure the Trading_bot_website directory is in the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Correct import statement
try:
    from Trading_bot_website.app.create_app import create_app  # ✅ Correct path
except ImportError as e:
    print(f"⚠️ ImportError: {e}")
    print("Check if 'Trading_bot_website/app/create_app.py' exists and '__init__.py' is present.")
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
