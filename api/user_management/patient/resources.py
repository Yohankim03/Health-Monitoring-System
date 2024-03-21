from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import Measurement, Appointment
import datetime

measurement_fields = {
    'id': fields.Integer,
    'patient_id': fields.Integer,
    'type': fields.String,
    'value': fields.Float,
    'unit': fields.String,
    'timestamp': fields.DateTime(dt_format='rfc822'),
}

appointment_fields = {
    'id': fields.Integer,
    'patient_id': fields.Integer,
    'professional_id': fields.Integer,
    'date': fields.String,
    'time': fields.String,
    'status': fields.String,
}


class PatientMeasurement(Resource):
    @marshal_with(measurement_fields)
    def post(self, patient_id):
        # Assume authentication is handled elsewhere and patient_id is retrieved from there
        parser = reqparse.RequestParser()
        parser.add_argument('type', required=True, help="Measurement type is required.")
        parser.add_argument('value', type=float, required=True, help="Measurement value is required.")
        parser.add_argument('unit', required=True, help="Measurement unit is required.")
        parser.add_argument('timestamp', required=False)  # This could be auto-generated
        args = parser.parse_args()

        # Create a new measurement instance
        new_measurement = Measurement(
            patient_id=patient_id,
            type=args['type'],
            value=args['value'],
            unit=args['unit'],
            timestamp=args.get('timestamp') or datetime.utcnow()
        )
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement
    
    @marshal_with(measurement_fields)
    def get(self, patient_id):
        measurements = Measurement.query.filter_by(patient_id=patient_id).all()
        return measurements


class PatientCommunication(Resource):
    def post(self, patient_id):
        parser = reqparse.RequestParser()
        parser.add_argument('message', required=True, help="Message content is required.")
        # Add arguments for recipient, subject, etc.
        args = parser.parse_args()

        # Here you would create a new message instance and save it
        # The implementation will depend on how messages are stored and processed
        pass

class PatientAppointment(Resource):
    @marshal_with(appointment_fields)
    def post(self, patient_id):
        parser = reqparse.RequestParser()
        parser.add_argument('date', required=True, help="Date of the appointment is required.")
        parser.add_argument('time', required=True, help="Time of the appointment is required.")
        # Add arguments for the medical professional's ID, reason for appointment, etc.
        args = parser.parse_args()

        # Create a new appointment instance
        new_appointment = Appointment(
            patient_id=patient_id,
            # Other details
        )
        db.session.add(new_appointment)
        db.session.commit()
        return new_appointment, 201
