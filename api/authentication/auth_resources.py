from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import User, Role
from flask_jwt_extended import create_access_token, create_refresh_token

user_profile_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String
}

class UserRegistration(Resource):
    @marshal_with(user_profile_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', help='This field cannot be blank', required=True)
        parser.add_argument('email', help='This field cannot be blank', required=True)
        parser.add_argument('password', help='This field cannot be blank', required=True)
        data = parser.parse_args()
        
        if User.query.filter_by(username=data['username']).first():
            return {'message': 'User {} already exists'.format(data['username'])}
        
        new_user = User(username=data['username'], email=data['email'])
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
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 404
        
        if current_user.check_password(data['password']):
            access_token = create_access_token(identity=data['username'])
            refresh_token = create_refresh_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token,
                'refresh_token': refresh_token
                }, 200
        else:
            return {'message': 'Wrong credentials'}, 401