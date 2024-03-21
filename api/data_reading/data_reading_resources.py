from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import Measurement
from  datetime import datetime

measurement_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'type': fields.String,
    'value': fields.Float,
    'unit': fields.String,
    'timestamp': fields.DateTime,
}

class MeasurementResource(Resource):
    @marshal_with(measurement_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True, help="User ID is required")
        parser.add_argument('type', required=True, help="Type of measurement is required")
        parser.add_argument('value', type=float, required=True, help="Value of measurement is required")
        parser.add_argument('unit', required=True, help="Unit of measurement is required")
        args = parser.parse_args()

        new_measurement = Measurement(
            user_id=args['user_id'],
            type=args['type'],
            value=args['value'],
            unit=args['unit'],
            timestamp=datetime.utcnow()
        )
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201
    
class MeasurementListResource(Resource):
    @marshal_with(measurement_fields)
    def get(self, user_id):
        measurements = Measurement.query.filter_by(user_id=user_id).order_by(Measurement.timestamp.desc()).all()
        return measurements
