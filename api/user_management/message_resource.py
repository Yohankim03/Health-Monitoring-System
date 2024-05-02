from flask_restful import Resource, reqparse, fields, marshal_with
from api.models import Message
from extensions import db

message_fields = {
    'id': fields.Integer,
    'sender_id': fields.Integer,
    'receiver_id': fields.Integer,
    'content': fields.String,
    'timestamp': fields.DateTime,
}

class SendMessage(Resource):
    @marshal_with(message_fields)
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('sender_id', type=int, required=True, help="Sender ID is required")
        parser.add_argument('receiver_id', type=int, required=True, help="Receiver ID is required")
        parser.add_argument('content', required=True, help="Message content is required")
        args = parser.parse_args()

        message = Message(sender_id=args['sender_id'], receiver_id=args['receiver_id'], content=args['content'])
        db.session.add(message)
        db.session.commit()
        return message, 201

class RetrieveMessages(Resource):
    @marshal_with(message_fields)
    def get(self, user_id):
        messages = Message.query.filter((Message.sender_id == user_id) | (Message.receiver_id == user_id)).all()
        return messages
