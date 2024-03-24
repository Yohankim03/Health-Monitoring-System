from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import Report, Measurement, DeviceAssignment, Device
from extensions import db
from queue_manager import task_queue
from tasks import generate_report_task

class DateField(fields.Raw):
    def format(self, value):
        return value.strftime('%m-%d-%Y')  # Formats the date as MM-DD-YYYY

report_fields = {
    'id': fields.Integer,
    'generated_by': fields.Integer,
    'patient_id': fields.Integer,
    'content': fields.String,
    'timestamp': DateField(),
}

# class CreateReport(Resource):
#     @marshal_with(report_fields)
#     def post(self):
#         parser = reqparse.RequestParser()
#         parser.add_argument('generated_by', type=int, required=True, help="User ID of the report creator is required")
#         parser.add_argument('patient_id', type=int, required=True, help="Patient ID the report is about is required")
#         args = parser.parse_args()

#         # Fetch measurements for the patient
#         measurements = Measurement.query.filter_by(user_id=args['patient_id']).all()
#         # Fetch devices assigned to the patient
#         device_assignments = DeviceAssignment.query.filter_by(patient_id=args['patient_id']).all()

#         # Generate report content
#         report_content = "Patient Report\n\n"
#         report_content += "Measurements:\n"
#         for measurement in measurements:
#             report_content += f"Type: {measurement.type}, Value: {measurement.value} {measurement.unit}, Timestamp: {measurement.timestamp}\n"
        
#         report_content += "\nDevices Assigned:\n"
#         for assignment in device_assignments:
#             device = Device.query.get(assignment.device_id)
#             report_content += f"Device Name: {device.name}, Assigned On: {assignment.assigned_on}\n"

#         # Create the new report
#         new_report = Report(
#             generated_by=args['generated_by'],
#             patient_id=args['patient_id'],
#             content=report_content
#         )
#         db.session.add(new_report)
#         db.session.commit()
#         return new_report, 201

class CreateReport(Resource):
    @marshal_with(report_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('generated_by', type=int, required=True)
        parser.add_argument('patient_id', type=int, required=True)
        args = parser.parse_args()

        # Enqueue the report generation task
        task_queue.put((generate_report_task, (args['generated_by'], args['patient_id'])))

        return {'message': 'Report generation has been queued'}, 202

class ListReports(Resource):
    @marshal_with(report_fields)
    def get(self):
        reports = Report.query.all()
        return reports

class GetReport(Resource):
    @marshal_with(report_fields)
    def get(self, report_id):
        report = Report.query.get_or_404(report_id)
        return report
