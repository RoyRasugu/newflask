from flask import Flask
import os
from .auth.v1 import version_1_auth
from .auth.v1.models.db_model import Quora_Db
from config import app_config 
from flask_jwt_extended import JWTManager
from datetime import timedelta

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    with app.app_context():
        Quora_Db.init_db(app.config.get('DB_NAME'),app.config.get('DB_HOST'),app.config.get('DB_PASSWORD'),app.config.get('DB_USER'))
        Quora_Db.build_tables()

    app.register_blueprint(version_1_auth)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=6)
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    jwt = JWTManager(app)

    return app
