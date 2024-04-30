from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import User, Role
from extensions import db

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
    'first_name': fields.String,
    'last_name': fields.String
}



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
