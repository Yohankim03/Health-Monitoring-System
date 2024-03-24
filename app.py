# Import Flask, SQLAlchemy, Migrate, and create_api function
from flask import Flask
from extensions import db
from flask_migrate import Migrate
from api import create_api
from api.models import Role, User, Device
from werkzeug.security import generate_password_hash
from flask_jwt_extended import JWTManager
import os

# Create the Flask application
app = Flask(__name__)

# Configure the database URI and disable track modifications for performance
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'secret_key'  # Change this to a random secret key

# Initialize the database with the app
db.init_app(app)

# Set up Flask-Migrate
migrate = Migrate(app, db)

# Call create_api to set up the API routes
api = create_api(app)
jwt = JWTManager(app)

def create_roles():
    roles = ["Admin", "Patient", "Medical Professional"]  # Add all roles you need
    for role_name in roles:
        if not Role.query.filter_by(name=role_name).first():
            new_role = Role(name=role_name)
            db.session.add(new_role)
    db.session.commit()
    
def add_devices():
    devices = ["Heart Rate Monitor", "Blood Pressure Monitor", ""]  # Add all roles you need
    for device in devices:
        if not Device.query.filter_by(name=device).first():
            new_device = Device(name=device, status="active")
            db.session.add(new_device)
    db.session.commit()
    
def insert_test_data():

    # Fetch roles
    admin_role = Role.query.filter_by(name='Admin').first()
    patient_role = Role.query.filter_by(name='Patient').first()
    medical_professional_role = Role.query.filter_by(name='Medical Professional').first()

    # Check if we already have users to avoid duplicating test data
    if not User.query.first():
        # Create and add admin user
        admin_user = User(username='admin', email='admin@example.com',
                            password_hash=generate_password_hash('admin123'))
        admin_user.roles.append(admin_role)
        db.session.add(admin_user)

        # Create and add patient user
        patient_user = User(username='patient', email='patient@example.com',
                            password_hash=generate_password_hash('patient123'))
        patient_user.roles.append(patient_role)
        db.session.add(patient_user)

        # Create and add medical professional user
        mp_user = User(username='medpro', email='medpro@example.com',
                        password_hash=generate_password_hash('medpro123'))
        mp_user.roles.append(medical_professional_role)
        db.session.add(mp_user)

        db.session.commit()

# Run the application
if __name__ == '__main__':
    with app.app_context():
        create_roles()
        add_devices()
        insert_test_data()

    app.run(debug=True)
