from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
#from models import Measurement, Device, DeviceAssignment, Patient
from api.models import Patient
import datetime

patient_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
}

add_patient_parser = reqparse.RequestParser()
add_patient_parser.add_argument('first_name', type=str, required=True, help="First name is required")
add_patient_parser.add_argument('last_name', type=str, required=True, help="Last name is required")

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