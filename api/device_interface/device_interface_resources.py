from flask_restful import Resource, fields, marshal_with, reqparse, abort
from extensions import db
from api.models import Measurement, Device, DeviceAssignment
import datetime

class DateField(fields.Raw):
    def format(self, value):
        return value.strftime('%m-%d-%Y')

device_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'status': fields.String,
}

device_assignment_fields = {
    'id': fields.Integer,
    'patient_id': fields.Integer,
    'device_id': fields.Integer,
    'status': fields.String,
    'assigned_on': DateField()
}

class AddDevice(Resource):
    @marshal_with(device_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="Name of the device is required")
        args = parser.parse_args()

        new_device = Device(
            name=args['name'],
            status='inactive',  # default status
        )
        db.session.add(new_device)
        db.session.commit()
        return new_device, 201
    
class AssignDevice(Resource):
    @marshal_with(device_assignment_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', type=int, required=True, help="Patient ID is required")
        parser.add_argument('device_id', type=int, required=True, help="Device ID is required")
        args = parser.parse_args()

        # Additional checks can be made here to confirm patient and device exist and are valid
        new_assignment = DeviceAssignment(
            patient_id=args['patient_id'],
            device_id=args['device_id'],
        )
        db.session.add(new_assignment)
        db.session.commit()
        return new_assignment, 201


class UpdateDeviceStatus(Resource):
    @marshal_with(device_fields)
    def put(self, device_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True, help="New status is required")
        args = parser.parse_args()

        device = Device.query.get_or_404(device_id)
        device.status = args['status']
        db.session.commit()
        return device

class ListDevices(Resource):
    @marshal_with(device_fields)
    def get(self):
        devices = Device.query.all()
        return devices
