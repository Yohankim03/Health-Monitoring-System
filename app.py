# Import Flask, SQLAlchemy, Migrate, and create_api function
from flask import Flask
from extensions import db
from flask_migrate import Migrate
from api import create_api
import os

# Create the Flask application
app = Flask(__name__)

# Configure the database URI and disable track modifications for performance
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db)

# Call create_api to set up the API routes
api = create_api(app)


# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
