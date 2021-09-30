from .db_model import Quora_Db
import jwt
from datetime import datetime, timedelta
from flask import current_app
from werkzeug.security import generate_password_hash,check_password_hash

class UserModels():
    """
    Class for the user operations
    """
    
    def create_user(self, username, email, userpassword, confirm_password):
        """
        Method to create a new user record
        """
        hashed_password = generate_password_hash(userpassword)
        email_query = """SELECT * FROM users WHERE email = '{}'""".format(email)
        duplicate_email = Quora_Db.retrieve_all(email_query)
        if duplicate_email:
            return False

        user_query = """
        INSERT INTO users (username, email, userpassword, confirm_password)
        VALUES(%s, %s, %s, %s)
        RETURNING email, username
        """
        user_data = (username, email, hashed_password, confirm_password)

        response = Quora_Db.add_to_db(user_query, user_data)
        return response

    def get_user_by_email(self, email):
        """Get user by email"""
        user_email_query = f"SELECT * FROM users WHERE email = {email}"
        user_response = Quora_Db.retrieve_one(user_email_query)
        if not user_response:
            return False
        return user_response

    def get_user_by_id(self, id):
        """Get a user by id"""
        user_id_query = """SELECT * FROM users WHERE userId = '{}'""".format(
            id)
        user_response = Quora_Db.retrieve_one(user_id_query)
        if not user_response:
            return False
        return user_response

    def validate_password(self, userpassword, user_email):
        """Method to check if password matches"""
        query = """SELECT userpassword FROM users where email='{}'""".format(
            user_email)
        result = Quora_Db.retrieve_one(query)

        if not check_password_hash(result['userpassword'], userpassword):
            return False
        return True

    def generate_token(self, email):
        """Method to generate token"""
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=60),
                'iat': datetime.utcnow(),
                'email': email,
            }
            token = jwt.encode(
                payload,
                str(current_app.config.get('SECRET')),
                algorithm='HS256'
            )
            return token
        except Exception as e:
            return str(e)

    @staticmethod
    def decode_token(token):
        '''Method for decoding token generated'''
        token_payload = jwt.decode(token, str(
            current_app.config.get('SECRET')), algorithms=['HS256'])
        return token_payload   
