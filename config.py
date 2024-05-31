import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DEBUG = False
    SECRET_KEY = str(os.environ.get('SECRET_KEY'))
    WTF_CSRF_SECRET_KEY = str(os.environ.get('WTF_CSRF_SECRET_KEY'))
    SQLALCHEMY_DATABASE_URI = str(os.environ.get(
        'DATABASE_URL')) + str(os.environ.get('DATABASE_NAME'))

    SQLALCHEMY_TRACK_MODIFICATIONS = False
