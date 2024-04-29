# Import Flask-RESTful Api and all resources
from flask_restful import Api
from .authentication.auth_resources import UserRegistration, UserLogin
from .notifcation.noti_resources import NotificationResource
from .data_reading.data_reading_resources import AddMeasurement, ViewMeasurement
from .device_interface.device_interface_resources import AddDevice, AssignDevice, UpdateDeviceStatus, ListDevices
from .report.report_resources import CreateReport, ListReports, GetReport
from .user_management.user_man_resources import DeleteUser, GetUsers
from .user_management.admin_resources import AdminManageUserRoles

# Define the create_api function
def create_api(app):
    api = Api(app)
    
    # Auth
    api.add_resource(UserRegistration, '/registration')
    api.add_resource(UserLogin, '/login')
    
    # Notificaiton
    api.add_resource(NotificationResource, '/notification', '/notification/<int:user_id>')
    
    # Data Reading
    api.add_resource(AddMeasurement, '/users/<string:username>/addmeasurements')
    api.add_resource(ViewMeasurement, '/users/<string:username>/measurements')
    
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
    api.add_resource(AdminManageUserRoles, '/admin/<int:user_id>/change_role')
    
    
    
    return api
