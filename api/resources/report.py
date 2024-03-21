from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import Report
from extensions import db

report_fields = {
    'id': fields.Integer,
    'generated_by': fields.Integer,
    'patient_id': fields.Integer,
    'content': fields.String,
    'timestamp': fields.DateTime,
}

report_parser = reqparse.RequestParser()
report_parser.add_argument('generated_by', type=int, required=True, help='ID of medical professional required.')
report_parser.add_argument('patient_id', type=int, required=True, help='ID of patient required.')
report_parser.add_argument('content', type=str, required=True, help='Content of report required.')

class ReportResource(Resource):
    @marshal_with(report_fields)
    def post(self):
        args = report_parser.parse_args()
        new_report = Report(generated_by=args['generated_by'], patient_id=args['patient_id'], content=args['content'])
        db.session.add(new_report)
        db.session.commit()
        return new_report, 201
    
    @marshal_with(report_fields)
    def get(self):
        report = Report.query.all()
        return report