from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import Measurement, User
from  datetime import date

class DateField(fields.Raw):
    def format(self, value):
        return value.strftime('%m-%d-%Y')

measurement_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'type': fields.String,
    'value': fields.Float,
    'unit': fields.String,
    'timestamp': DateField(),
}

class AddMeasurement(Resource):
    @marshal_with(measurement_fields)
    def post(self, username):
        parser = reqparse.RequestParser()
        #parser.add_argument('user_id', type=int, required=True, help="User ID is required")
        parser.add_argument('type', required=True, help="Type of measurement is required")
        parser.add_argument('value', type=float, required=True, help="Value of measurement is required")
        parser.add_argument('unit', required=True, help="Unit of measurement is required")
        args = parser.parse_args()
        
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': f'User with username {username} not found'}, 404

        new_measurement = Measurement(
            user_id=user.id,
            type=args['type'],
            value=args['value'],
            unit=args['unit'],
            timestamp=date.today()
        )
        db.session.add(new_measurement)
        db.session.commit()
        return new_measurement, 201
    
class ViewMeasurement(Resource):
    @marshal_with(measurement_fields)
    def get(self, username):
        # First, find the user by username to get the user_id
        user = User.query.filter_by(username=username).first()
        if not user:
            return {'message': 'User not found'}, 404

        # Then, retrieve measurements for that user
        measurements = Measurement.query.filter_by(user_id=user.id).order_by(Measurement.timestamp.desc()).all()
        return measurements
