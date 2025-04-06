# import os
# from dotenv import load_dotenv
from credentials import DATABASE_URL, SECRET_KEY, JWT_SECRET_KEY, REDIS_URL
# load_dotenv()  # Load environment variables from .env file

class Config:
    # load credentials from the credentials.py file
    # load_dotenv() method can also use if credentials are store in .env file
    # Load environment variables from .env file 
    SECRET_KEY = SECRET_KEY
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = JWT_SECRET_KEY
    REDIS_URL = REDIS_URL
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL