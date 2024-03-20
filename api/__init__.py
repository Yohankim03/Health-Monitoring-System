# Import Flask-RESTful Api and all resources
from flask_restful import Api
from .resources.device import GetDeviceStatus, EnableDisableDevice, AssignDeviceToPatient, AddDevice, MeasurementListAPI
from .resources.patient import AddPatient

# Define the create_api function
def create_api(app):
    api = Api(app)
    # Add resources and their endpoints
    api.add_resource(MeasurementListAPI, '/patients/<int:patient_id>/measurements')
    api.add_resource(AddDevice, '/devices')
    api.add_resource(AssignDeviceToPatient, '/devices/assign')
    api.add_resource(GetDeviceStatus, '/devices/<int:deviceId>/status')
    api.add_resource(EnableDisableDevice, '/devices/<int:deviceId>/enable')
    api.add_resource(AddPatient, '/patients')
    
    return api
