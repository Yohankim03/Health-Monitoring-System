from flask_restful import Resource, fields, marshal_with, reqparse, abort
from extensions import db
from models import Measurement, Device, DeviceAssignment, Patient
import datetime
from flask import jsonify

# Define the output structure
measurement_fields = {
    'id': fields.Integer,
    'patient_id': fields.Integer,
    'type': fields.String,
    'value': fields.Float,
    'unit': fields.String,
    'timestamp': fields.DateTime,
}

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

patient_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
}


# Define input parsing
measurement_parser = reqparse.RequestParser()
measurement_parser.add_argument('type', required=True, help="Type of measurement cannot be blank")
measurement_parser.add_argument('value', type=float, required=True, help="Value of measurement cannot be blank")
measurement_parser.add_argument('unit', required=True, help="Unit cannot be blank")

device_parser = reqparse.RequestParser()
device_parser.add_argument('patientId', type=int, required=True, help="Patient ID is required")
device_parser.add_argument('deviceId', type=int, required=False, help="Device ID is required")
device_parser.add_argument('assignmentDetails', required=False)
device_parser.add_argument('isEnabled', type=bool, required=False, help="Enabled status is required for enabling/disabling a device")

device_creation_parser = reqparse.RequestParser()
device_creation_parser.add_argument('name', type=str, required=True, help="Name of the device is required")
device_creation_parser.add_argument('status', type=str, required=True, help="Status of the device is required")

add_patient_parser = reqparse.RequestParser()
add_patient_parser.add_argument('first_name', type=str, required=True, help="First name is required")
add_patient_parser.add_argument('last_name', type=str, required=True, help="Last name is required")

class MeasurementListAPI(Resource):
    @marshal_with(measurement_fields)
    def get(self, patient_id):
        return Measurement.query.filter_by(patient_id=patient_id).all()

    @marshal_with(measurement_fields)
    def post(self, patient_id):
        args = measurement_parser.parse_args()
        new_measurement = Measurement(
            patient_id=patient_id,
            type=args['type'],
            value=args['value'],
            unit=args['unit'],
            timestamp=datetime.datetime.now()  # Correctly uses datetime
        )
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201

    def delete(self, measurement_id):
        measurement = Measurement.query.get(measurement_id)
        if measurement:
            db.session.delete(measurement)
            db.session.commit()
            return '', 204  # No content response
        else:
            return {'message': 'Measurement not found'}, 404

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
    
class AddPatient(Resource):
    @marshal_with(patient_fields)
    def post(self):
        args = add_patient_parser.parse_args()
        new_patient = Patient(first_name=args['first_name'], last_name=args['last_name'])
        db.session.add(new_patient)
        db.session.commit()
        return new_patient, 201
    
    @marshal_with(patient_fields)
    def get(self):
        patients = Patient.query.all()
        return patients