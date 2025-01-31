import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_DATABASE_URI = "mysql://dcims:dcims_password@localhost/dcims"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_FILE = '/opt/dcims/logs/dcims.log'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size