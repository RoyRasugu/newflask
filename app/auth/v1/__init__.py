from flask import Blueprint
from flask_restful import Api
from . views.user_views import UserRegister, UserLogin

version_1_auth = Blueprint('auth_v1', __name__, url_prefix='/auth/v1')

api = Api(version_1_auth)

api.add_resource(UserRegister, '/signup')
api.add_resource(UserLogin, '/login')

# http://127.0.0.1:5000/auth/v1/signup
# http://127.0.0.1:5000/auth/v1/login