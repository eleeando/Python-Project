from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE

class Message:
    def __init__(self,data):
        self.id=data=['id']
        self.sender_id=data['sender_id']
        self.reciver_id=data['reciver_id']
        self.house_id=data['house_id']
        self.context=data['context']
        self.created_at=data['created_at']
        self.updated_at=data['updated_at']


    @classmethod
    def create_a_message(cls,data):
        query="""INSERT INTO messages (sender_id,receiver_id,house_id,context)
                VALUES
                (%(sender_id)s,%(receiver_id)s,%(house_id)s,%(context)s);"""
        return connectToMySQL(DATABASE).query_db(query,data)
    
    @classmethod
    def show_one_conversation(cls,data):
        query="""SELECT * FROM messages WHERE
                    sender_id=%(sender_id)s AND receiver_id=%(receiver_id)s AND house_id=%(house_id)s ;"""
        results=connectToMySQL(DATABASE).query_db(query,data)
        conversations=[]
        for conversation in results:
            conversations.append(cls(conversation))
        return conversations