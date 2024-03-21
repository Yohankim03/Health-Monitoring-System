from extensions import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class Measurement(db.Model):
    __tablename__ = 'measurement'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    type = db.Column(db.String, nullable=False)
    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    patient = db.relationship('Patient', back_populates='measurements')

    def __repr__(self):
        return f'<Measurement {self.type}>'

class Device(db.Model):
    __tablename__ = 'device'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), nullable=False, default="inactive")
    assignments = db.relationship('DeviceAssignment', backref='device', lazy=True)

class DeviceAssignment(db.Model):
    __tablename__ = 'device_assignment'
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'), nullable=False)
    assignment_details = db.Column(db.String(200))
    assigned_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    patient = db.relationship('Patient', back_populates='device_assignments')

class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    dob = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(50))
    contact_number = db.Column(db.String(50))
    
    measurements = db.relationship('Measurement', back_populates='patient', lazy='dynamic')
    device_assignments = db.relationship('DeviceAssignment', back_populates='patient')
    reports = db.relationship('Report', back_populates='patient', lazy='dynamic')

    def __repr__(self):
        return f'<Patient {self.first_name} {self.last_name}>'

# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(50), nullable=False, unique=True)
#     email = db.Column(db.String(100), nullable=False, unique=True)
#     password_hash = db.Column(db.String(255), nullable=False)
#     role = db.Column(db.String(100), nullable=False)
    
#     patient = db.relationship('Patient', backref='user', lazy=True)
#     medical_professional = db.relationship('MedicalProfessional', backref='user', lazy=True)
    
#     def __init__(self, username, email, password, role):
#         self.username = username
#         self.email = email
#         self.password_hash = generate_password_hash(password)
#         self.role = role
    
#     def __repr__(self):
#         return f'<User {self.username} {self.role}>'
    
class Report(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True)
    generated_by = db.Column(db.Integer, db.ForeignKey('medical_professional.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    medical_professional = db.relationship('MedicalProfessional', back_populates='reports')
    patient = db.relationship('Patient', back_populates='reports')

    def __repr__(self):
        return f'<Report {self.id} for patient {self.patient_id}>'
    
class MedicalProfessional(db.Model):
    __tablename__ = 'medical_professional'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    contact_number = db.Column(db.String(50))
    email = db.Column(db.String(100), unique=True)
    
    user = db.relationship('User', backref=db.backref('medical_professional', uselist=False))
    reports = db.relationship('Report', back_populates='medical_professional')

    def __repr__(self):
        return f'<MedicalProfessional {self.title} {self.first_name} {self.last_name}>'
    
class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.String(50), nullable=False, default='unread')
    user = db.relationship('User', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.id}>'
    

# Association table for the many-to-many relationship
roles_users = db.Table('roles_users',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'), primary_key=True)
)
    
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

    def __repr__(self):
        return f'<Role {self.name}>'

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Relationships
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

    # def __init__(self, username, email, password, roles):
    #     self.username = username
    #     self.email = email
    #     self.password_hash = generate_password_hash(password)
    #     self.roles = roles  # This should be a list of Role instances
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
    
    def has_role(self, role_name):
        return any(role.name == role_name for role in self.roles)

    def __repr__(self):
        return f'<User {self.username}>'
