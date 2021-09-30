from flask import request
from flask_restful import Resource, reqparse
from app.auth.v1.models.user_models import UserModels
from flask_jwt_extended import create_access_token, create_refresh_token
from app.utilities.validation import check_email_format

user_model_view = UserModels()

class UserRegister(Resource):
    """
    User class view for register endpoint
    """

    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help='Please input your name')
    parser.add_argument('email', type=str, required=True, help='Please input an email')
    parser.add_argument('userpassword', type=str, required=True, help='Please input your password')
    parser.add_argument('confirm_password', type=str, required=True, help='Ensure the passwords match')

    def post(self):
        """
        HTTP method to register a new user
        """
        try:
            args = UserRegister.parser.parse_args()
            username = args.get('username')
            email = args.get('email')
            userpassword = args.get('userpassword')
            confirm_password = args.get('confirm_password')
            
        except Exception as e:
            return {
                "status": 400,
                "error": "Invalid Key error {}".format(e)
            }, 400

        if not check_email_format(email):
            return {
                "status": 400,
                "message":
                "Email format is incorrect, its should be",
                "Email Format": "name@company.[com|org|edu" 
            }, 400

        access_token = create_access_token(identity=args.get('email'))
        renewal_token = create_refresh_token(identity=args.get('email'))
        
        new_user = user_model_view.create_user(username=username, email=args.get('email'),userpassword = userpassword,confirm_password= confirm_password)
        return {
            "status": 201,
            "Token": access_token,
            "Refresh Token": renewal_token,
            "data": new_user
        }, 201

class UserLogin(Resource):
    """
    User class view to login a user
    """
    parser = reqparse.RequestParser()
    parser.add_argument("email", type=str, required=True, help="PLease input an email")
    parser.add_argument("userpassword", type=str, required=True, help="Please input your password")

    def post(self):
        """
        HTTP method to login a user
        """
        try:
            args = UserLogin.parser.parse_args()
            email = args.get('email'),
            userpassword = args.get('userpassword')
        
        except Exception as e:
            return {
                "status": 400,
                "error": "Invalid Key error. You should provide an email and password"
            }, 400

        new_email_format = str(email)[1:-1]
        nd_format = new_email_format.split(',')
        rd_format = nd_format[0]


        # import pdb; pdb.set_trace()

        user_email_exists = user_model_view.get_user_by_email(rd_format)
        # it will return the user info

        if not user_email_exists:
            return {
                "status": 404,
                "error": "You need a valid email address to login"
            }, 404

        for data in user_email_exists:
            response = {
                "id": user_email_exists["userid"],
                "email": user_email_exists["email"]
            }

        return {
            "status": 201, 
            "data":[{ 
                "Token": create_access_token(identity=args.get('email')),
                "user": response
            }
            ]
        }, 201

