from Trading_bot_website.app.create_app import create_app
from flask import render_template

app = create_app()
# Define a simple route to serve index.html
@app.route('/')  # This is the home route
def home():
    return render_template('index.html')  # Ensure this file exists inside `templates/`