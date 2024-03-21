from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import Patient, Measurement, DeviceAssignment
import datetime

patient_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
}

# class BrowsePatients(Resource):
#     @marshal_with(patient_fields)  # Ensure you have defined patient_fields correctly
#     def get(self):
#         # This check assumes you have a way to verify if the user is an MP or has higher privileges
#         if current_user.is_admin() or current_user.is_medical_professional():
#             patients = Patient.query.all()
#         else:
#             # If not admin or MP, perhaps return only their assigned patients
#             patients = Patient.query.filter_by(assigned_mp_id=current_user.id).all()
#         return patients

class AssignDeviceToPatient(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', type=int, required=True, help="Patient ID is required.")
        parser.add_argument('device_id', type=int, required=True, help="Device ID is required.")
        args = parser.parse_args()

        # Additional checks to ensure that the MP has privileges to assign devices may be added here

        assignment = DeviceAssignment(
            patient_id=args['patient_id'],
            device_id=args['device_id'],
            # Assume we handle assignment details and timestamps inside the DeviceAssignment model
        )
        db.session.add(assignment)
        db.session.commit()
        return {"message": "Device assigned successfully."}, 201

class InputPatientData(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('patient_id', type=int, required=True)
        parser.add_argument('type', type=str, required=True)
        parser.add_argument('value', type=float, required=True)
        parser.add_argument('unit', type=str, required=True)
        # Assume that timestamp is generated automatically by the server
        args = parser.parse_args()

        # Additional checks to ensure the MP can input data for this patient

        measurement = Measurement(
            patient_id=args['patient_id'],
            type=args['type'],
            value=args['value'],
            unit=args['unit'],
            timestamp=datetime.utcnow()
        )
        db.session.add(measurement)
        db.session.commit()
        return {"message": "Measurement input successfully."}, 201



# class SendMessage(Resource):
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('patient_id', type=int, required=True)
#         parser.add_argument('content', type=str, required=True)
#         args = parser.parse_args()

#         # You'd need a Message model and ensure the MP can message this patient

#         message = Message(
#             sender_id=current_user.id,  # Assuming current_user is available and is the sender
#             receiver_id=args['patient_id'],
#             content=args['content'],
#             # Assume timestamps are handled automatically
#         )
#         db.session.add(message)
#         db.session.commit()
#         return {"message": "Message sent successfully."}, 201

# class AppointmentResource(Resource):
#     def post(self):
#         # Parse request for appointment details
#         # Create an Appointment object
#         # Add to database and return a success message

#     def get(self, appointment_id):
#         # Retrieve an appointment by ID

#     def put(self, appointment_id):
#         # Update an existing appointment

#     def delete(self, appointment_id):
#         # Delete an appointment
