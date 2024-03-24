# Import Flask-RESTful Api and all resources
from flask_restful import Api
from .authentication.auth_resources import UserRegistration, UserLogin
from .notifcation.noti_resources import NotificationResource
from .data_reading.data_reading_resources import MeasurementResource, MeasurementListResource
from .device_interface.device_interface_resources import AddDevice, AssignDevice, UpdateDeviceStatus, ListDevices
from .report.report_resources import CreateReport, ListReports, GetReport
from .user_management.user_man_resources import DeleteUser, GetUsers

# Define the create_api function
def create_api(app):
    api = Api(app)
    
    # Auth
    api.add_resource(UserRegistration, '/registration')
    api.add_resource(UserLogin, '/login')
    
    # Notificaiton
    api.add_resource(NotificationResource, '/notification', '/notification/<int:user_id>')
    
    # Data Reading
    api.add_resource(MeasurementResource, '/measurements')
    api.add_resource(MeasurementListResource, '/users/<int:user_id>/measurements')
    
    # Device Interface
    api.add_resource(AddDevice, '/devices')
    api.add_resource(AssignDevice, '/devices/assign')
    api.add_resource(UpdateDeviceStatus, '/devices/<int:device_id>/status')
    api.add_resource(ListDevices, '/devices')

    #Reports
    api.add_resource(CreateReport, '/reports')
    api.add_resource(ListReports, '/reports')
    api.add_resource(GetReport, '/reports/<int:report_id>')

    # User Management
    api.add_resource(GetUsers, '/users')
    api.add_resource(DeleteUser, '/users/<int:id>/delete')
    
    
    return api
