from flask_restful import Resource, fields, marshal_with, reqparse, abort
from extensions import db
from models import Measurement, Device, DeviceAssignment, Patient
import datetime

device_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'status': fields.String,
}

assignment_fields = {
    'id': fields.Integer,
    'patient_id': fields.Integer,
    'device_id': fields.Integer,
    'assignment_details': fields.String,
    'assigned_on': fields.DateTime,
}

device_parser = reqparse.RequestParser()
device_parser.add_argument('patientId', type=int, required=True, help="Patient ID is required")
device_parser.add_argument('deviceId', type=int, required=False, help="Device ID is required")
device_parser.add_argument('assignmentDetails', required=False)
device_parser.add_argument('isEnabled', type=bool, required=False, help="Enabled status is required for enabling/disabling a device")

device_creation_parser = reqparse.RequestParser()
device_creation_parser.add_argument('name', type=str, required=True, help="Name of the device is required")
device_creation_parser.add_argument('status', type=str, required=True, help="Status of the device is required")

class AddDevice(Resource):
    @marshal_with(device_fields)
    def post(self):
        args = device_creation_parser.parse_args()
        new_device = Device(name=args['name'], status=args['status'])
        db.session.add(new_device)
        db.session.commit()
        return new_device, 201
    
    @marshal_with(device_fields)
    def get(self):
        devices = Device.query.all()
        return devices
# {
#   "name": "Blood Pressure Monitor",
#   "status": "active"
# }

class AssignDeviceToPatient(Resource):
    @marshal_with(assignment_fields)
    def post(self):
        args = device_parser.parse_args()

        # Check if the patient exists
        
        # ADDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD
        # patient = Patient.query.get(args['patientId'])
        # if not patient:
        #     abort(404, message="Patient not found")

        # Check if the device exists
        device = Device.query.get(args['deviceId'])
        if not device:
            abort(404, message="Device not found")

        # Check if the device is already assigned
        existing_assignment = DeviceAssignment.query.filter_by(device_id=args['deviceId']).first()
        if existing_assignment:
            abort(400, message="Device is already assigned")

        new_assignment = DeviceAssignment(patient_id=args['patientId'], device_id=args['deviceId'], assignment_details=args.get('assignmentDetails', ''))
        db.session.add(new_assignment)
        db.session.commit()
        return new_assignment, 201
# {
#   "patientId": 4,
#   "deviceId": 1,
#   "assignmentDetails": "Assigned for blood pressure monitoring"
# }
    
class GetDeviceStatus(Resource):
    @marshal_with(device_fields)
    def get(self, deviceId):
        device = Device.query.get_or_404(deviceId)
        return device

class EnableDisableDevice(Resource):
    @marshal_with(device_fields)
    def put(self, deviceId):
        args = device_parser.parse_args()
        
        # Fetch the device to ensure it exists
        device = Device.query.get_or_404(deviceId)

        # Assuming you have an Assignment model that links devices to patients
        # Check if the device is assigned to the specified patient
        assignment = DeviceAssignment.query.filter_by(device_id=deviceId, patient_id=args['patientId']).first()
        if not assignment:
            abort(404, message="Device not assigned to this patient")

        # If the device is assigned to the patient, update the status
        device.status = "active" if args['isEnabled'] else "inactive"
        db.session.commit()
        
        return device