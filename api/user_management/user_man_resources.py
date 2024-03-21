from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import User
from extensions import db

user_fields = {
    'id': fields.Integer,
    'username': fields.String,
    'email': fields.String,
}



class GetUsers(Resource):
    @marshal_with(user_fields)
    def get(self):
        # parser = reqparse.RequestParser()
        # parser.add_argument('role', store_missing=False)
        # args = parser.parse_args()
        
        # query = User.query
        # if 'role' in args:
        #     query = query.filter_by(role=args['role'])
        # users = query.all()
        users = User.query.all()
        return users


class DeleteUser(Resource):
    def delete(self, id):
        user = User.query.get_or_404(id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}, 204
