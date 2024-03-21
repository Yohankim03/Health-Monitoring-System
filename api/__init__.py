# Import Flask-RESTful Api and all resources
from flask_restful import Api
from .resources.device import GetDeviceStatus, EnableDisableDevice, AssignDeviceToPatient, AddDevice, MeasurementListAPI
from .resources.patient import AddPatient
from .resources.notification import NotificationResource
from .resources.report import ReportResource
from .user_management.admin.resources import AdminAddUser, AdminManageUserRoles
from .user_management.medical_professional.resources import AssignDeviceToPatient, InputPatientData#, SendMessage, BrowsePatients
from .authentication.resources import UserRegistration, UserLogin

# Define the create_api function
def create_api(app):
    api = Api(app)
    # Add resources and their endpoints
    # api.add_resource(MeasurementListAPI, '/patients/<int:patient_id>/measurements')
    # api.add_resource(AddDevice, '/devices')
    # api.add_resource(AssignDeviceToPatient, '/devices/assign')
    # api.add_resource(GetDeviceStatus, '/devices/<int:deviceId>/status')
    # api.add_resource(EnableDisableDevice, '/devices/<int:deviceId>/enable')
    
    api.add_resource(NotificationResource, '/notifications')

    api.add_resource(ReportResource, '/reports')
    
    api.add_resource(AdminAddUser, '/admin/users')
    api.add_resource(AdminManageUserRoles, '/admin/users/<int:user_id>/roles')
    
    # api.add_resource(BrowsePatients, '/patients')
    api.add_resource(AssignDeviceToPatient, '/patients/assign-device')
    api.add_resource(InputPatientData, '/patients/input-data')
    # api.add_resource(SendMessage, '/patients/send-message')
    
    api.add_resource(UserRegistration, '/registration')
    api.add_resource(UserLogin, '/login')
    
    
    return api
