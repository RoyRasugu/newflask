import os

class Config():
    '''
    Base configuration class with minimal settings
    '''
    DEBUG = False
    TESTING = False
    JWT_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')

class Development:
    DEBUG = True
    TESTING = False
    DB_NAME=os.environ.get('DB_NAME')
    DB_HOST =os.environ.get('DB_HOST')
    DB_PASSWORD=os.environ.get('DB_PASSWORD')
    DB_USER=os.environ.get('DB_USER')


app_config = {
    'development': Development
}
