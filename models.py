from extensions import db
from datetime import datetime

# class Measurement(db.Model):
#     __tablename__ = 'measurement'
#     id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.Integer, nullable=False)
#     type = db.Column(db.String, nullable=False)
#     value = db.Column(db.Float, nullable=False)
#     unit = db.Column(db.String, nullable=False)
#     timestamp = db.Column(db.DateTime, nullable=False)
    
#     def __init__(self, patient_id, type, value, unit, timestamp):
#         self.patient_id = patient_id
#         self.type = type
#         self.value = value
#         self.unit = unit
#         self.timestamp = timestamp

#     def __repr__(self):
#         return f'<Measurement {self.type}>'

# class Device(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100), nullable=False)
#     status = db.Column(db.String(50), nullable=False, default="inactive")  # Example statuses: active, inactive, malfunctioning

# class DeviceAssignment(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     patient_id = db.Column(db.Integer, nullable=False)
#     device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
#     assignment_details = db.Column(db.String(200))
#     assigned_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
#     device = db.relationship('Device', backref=db.backref('assignments', lazy=True))
    
# class Patient(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)

class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)

    # Relationship (if you need to access patient from a Measurement instance)
    patient = db.relationship('Patient', back_populates='measurements')

    def __repr__(self):
        return f'<Measurement {self.type}>'

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="inactive")

    # Relationship to DeviceAssignment
    assignments = db.relationship('DeviceAssignment', backref='device', lazy=True)

class DeviceAssignment(db.Model):
    __tablename__ = 'device_assignment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    assignment_details = db.Column(db.String(200))
    assigned_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # Relationship (if you need to access patient from a DeviceAssignment instance)
    patient = db.relationship('Patient', back_populates='device_assignments')

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)

    # Relationships
    measurements = db.relationship('Measurement', back_populates='patient', lazy=True)
    device_assignments = db.relationship('DeviceAssignment', back_populates='patient', lazy=True)

    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'
