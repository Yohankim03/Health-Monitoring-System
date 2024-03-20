from flask import Flask
from flask_restful import Api
from extensions import db
from resources import MeasurementListAPI, AssignDeviceToPatient, GetDeviceStatus, EnableDisableDevice, AddDevice, AddPatient
from flask_migrate import Migrate
import os

app = Flask(__name__)
api = Api(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# add new table
# migrate = Migrate(app, db) 
# from models import Patient

api.add_resource(MeasurementListAPI, '/patients/<int:patient_id>/measurements')
api.add_resource(
    MeasurementListAPI,
    '/measurements/<int:measurement_id>',
    endpoint='measurement'  # To differentiate from the list endpoint
)

api.add_resource(AddDevice, '/devices')
api.add_resource(AssignDeviceToPatient, '/devices/assign')
api.add_resource(GetDeviceStatus, '/devices/<int:deviceId>/status')
api.add_resource(EnableDisableDevice, '/devices/<int:deviceId>/enable')

api.add_resource(AddPatient, '/patients')



if __name__ == '__main__':
    # Initialize database
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist

    # Run the application
    app.run(debug=True)
