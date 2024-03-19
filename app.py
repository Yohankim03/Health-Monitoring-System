from flask import Flask
from flask_restful import Api, Resource, fields, marshal_with, reqparse
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
db = SQLAlchemy(app)

class Measurement(db.Model):
    __tablename__ = 'measurements'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(50), nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Measurement {self.type}: {self.value} {self.unit} at {self.timestamp}>"

measurement_fields = {
    'id': fields.Integer,
    'type': fields.String,
    'value': fields.Float, 
    'unit': fields.String, 
    'timestamp': fields.DateTime(dt_format='iso8601')
}

parser = reqparse.RequestParser()
parser.add_argument('type', type=str, required=True, help="Type of measurement is required")
parser.add_argument('value', type=float, required=True, help="Value of measurement is required")
parser.add_argument('unit', type=str, required=True, help="Unit of measurement is required")
parser.add_argument('timestamp', type=datetime, required=False, help="Timestamp of measurement is optional")

class MeasurementResource(Resource):
    
    @marshal_with(measurement_fields)
    def get(self, patient_id):
        measurement = Measurement.query.get(patient_id)
        if not measurement:
            return {'message': 'Measurement not found'}, 404
        return measurement

    @marshal_with(measurement_fields)
    def post(self):
        args = parser.parse_args()
        timestamp = args.get('timestamp') or datetime.utcnow()
        measurement = Measurement(type=args['type'], value=args['value'], unit=args['unit'], timestamp=timestamp)
        db.session.add(measurement)
        db.session.commit()
        return measurement, 201
        
    def delete(self, patient_id):
        measurement = Measurement.query.get(patient_id)
        if not measurement:
            return {'message': 'Measurement not found'}, 404
        db.session.delete(measurement)
        db.session.commit()
        return {'message': 'Measurement deleted'}, 200

api.add_resource(MeasurementResource, '/patients/<int:patient_id>/measurements')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
