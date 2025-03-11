import sys
import os
from flask import Flask, render_template
import create_app
# Ensure Trading_bot_website is in the system path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    from Trading_bot_website.app.create_app import create_app
except ImportError as e:
    print(f"⚠️ ImportError: {e}")
    print("Check if 'Trading_bot_website/app/create_app.py' exists and '__init__.py' is present.")
    sys.exit(1)

app = create_app()

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
# The code snippet above is a Flask application that serves an index.html file.
# The index.html file is located in the templates directory.