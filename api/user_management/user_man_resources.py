from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import User, Role
from extensions import db

# user_fields = {
#     'id': fields.Integer,
#     'username': fields.String,
#     'email': fields.String,
#     'first_name': fields.String,
#     'last_name': fields.String
# }

role_fields = {
    'id': fields.Integer,
    'name': fields.String
}

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String,
    'dob': fields.String,  # Marshaling the date as a string; adjust formatting as needed
    'gender': fields.String,
    'phone_number': fields.String,
    'roles': fields.List(fields.Nested(role_fields))  # Nested field for roles
}


class GetRoles(Resource):
    @marshal_with(role_fields)
    def get(self):
        roles = Role.query.all()
        
        return roles

class GetUsers(Resource):
    @marshal_with(user_fields)
    def get(self, username):
        current_user = User.query.filter_by(username=username).first()

        if not current_user:
            return {'message': 'User not found'}, 404

        # Check if the current user is a Medical Professional
        if 'Medical Professional' in [role.name for role in current_user.roles]:
            # Return all users with the Patient role
            users = User.query.join(User.roles).filter(Role.name == 'Patient').all()
        elif 'Admin' in [role.name for role in current_user.roles]:
            users = User.query.options(db.joinedload(User.roles)).all()
        else:
            # Alternatively, handle other roles or return an unauthorized message
            return {'message': 'Unauthorized to view all users'}, 403

        return users


class DeleteUser(Resource):
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 204
