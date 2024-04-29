from flask_restful import Resource, fields, marshal_with, reqparse
from extensions import db
from api.models import User, Role
import datetime

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'roles': fields.List(fields.Nested({
        'id': fields.Integer,
        'name': fields.String
    }))
}

class AdminAddUser(Resource):
    @marshal_with(user_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="Username cannot be blank.")
        parser.add_argument('email', type=str, required=True, help="Email cannot be blank.")
        parser.add_argument('password', type=str, required=True, help="Password cannot be blank.")
        parser.add_argument('roles', type=str, action='append', help="Roles cannot be blank.")  # This will allow a list of roles to be provided
        args = parser.parse_args()

        new_user = User(
            username=args['username'],
            email=args['email'],
        )
        
        new_user.set_password(args['password'])
        db.session.add(new_user)
        db.session.flush()  # This will assign an ID to new_user without committing the transaction

        # Add roles to the new user
        if args['roles']:
            for role_name in args['roles']:
                role = Role.query.filter_by(name=role_name).first()
                if role:
                    new_user.roles.append(role)
                else:
                    # Role doesn't exist, rollback and return error
                    db.session.rollback()
                    return {"message": f"Role '{role_name}' does not exist."}, 400

        db.session.commit()
        return new_user, 200

class AdminManageUserRoles(Resource):
    @marshal_with(user_fields)
    def put(self, user_id):
        parser = reqparse.RequestParser()
        parser.add_argument('roles', type=str, action='append', required=True, help="This field cannot be blank and must be a list of roles.")
        args = parser.parse_args()

        user = User.query.get_or_404(user_id)

        # Reset roles only if new roles are provided and valid
        new_roles = []
        for role_name in args['roles']:
            role = Role.query.filter_by(name=role_name).first()
            if not role:
                db.session.rollback()  # Roll back any changes if there's an error
                return {"message": f"Role '{role_name}' does not exist."}, 400
            new_roles.append(role)

        user.roles = new_roles  # Assign new roles once all are verified
        db.session.commit()
        return user, 200
