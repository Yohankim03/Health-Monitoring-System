from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import Notification
from extensions import db

notification_fields = {
    'id': fields.Integer,
    'user_id': fields.Integer,
    'message': fields.String,
    'timestamp': fields.DateTime,
    'status': fields.String
}

notification_parser = reqparse.RequestParser()
notification_parser.add_argument('user_id', type=int, required=True, help='User ID is requried.')
notification_parser.add_argument('message', type=str, required=True, help='Message is requried.')

class NotificationResource(Resource):
    @marshal_with(notification_fields)
    def post(self):
        args = notification_parser.parse_args()
        new_notification = Notification(user_id=args['user_id'], message=args['message'])
        db.session.add(new_notification)
        db.session.commit()
        return new_notification, 201
    
    @marshal_with(notification_fields)
    def get(self):
        notifications = Notification.query.all()
        return notifications