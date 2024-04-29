from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import User, Role
from flask_jwt_extended import create_access_token, create_refresh_token
from werkzeug.security import check_password_hash
from datetime import datetime
from flask import jsonify

user_profile_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class UserRegistration(Resource):
    @marshal_with(user_profile_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help='This field cannot be blank')
        parser.add_argument('email', required=True, help='This field cannot be blank')
        parser.add_argument('password', required=True, help='This field cannot be blank')
        parser.add_argument('first_name', required=True, help='This field cannot be blank!')
        parser.add_argument('last_name', required=True, help='This field cannot be blank')
        parser.add_argument('dob', required=True, help='This field cannot be blank', type=lambda x: datetime.strptime(x, '%Y-%m-%d'))
        parser.add_argument('gender', required=True, help='This field cannot be blank')
        parser.add_argument('phone_number', help='This field can be blank')
        data = parser.parse_args()

        if User.query.filter_by(username=data['username']).first():
            return {'message': f'User {data["username"]} already exists'}, 400
        
        new_user = User(
            username=data['username'],
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            dob=data['dob'],
            gender=data['gender'],
            phone_number=data['phone_number']
        )
        new_user.set_password(data['password'])
        
        default_role = Role.query.filter_by(name='Patient').first()
        if default_role:
            new_user.roles.append(default_role)
        
        db.session.add(new_user)
        db.session.commit()

        return new_user, 201

class UserLogin(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()

        current_user = User.query.filter_by(username=data['username']).first()

        if not current_user:
            return {'message': f'User {data["username"]} doesn\'t exist'}, 404

        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            user_data = {
                'username': current_user.username,
                'email': current_user.email,
                'roles': [role.name for role in current_user.roles],
                'first_name': current_user.first_name,
                'last_name': current_user.last_name,
                # Add more stuff if needed
            }

            return {
                'message': f'Logged in as {current_user.username}',
                'access_token': access_token,
                'refresh_token': refresh_token,
                'user': user_data  # Include comprehensive user details
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 401
