from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy extension
# Note: No need to pass the Flask application object here. It will be done in the app.py file
db = SQLAlchemy()
