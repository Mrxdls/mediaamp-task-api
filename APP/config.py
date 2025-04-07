import os
from dotenv import load_dotenv
from urllib.parse import urlparse

# Load environment variables from .env file
load_dotenv()

REDIS_URL = os.getenv("REDIS_URL")  # Define REDIS_URL as a standalone variable

# Parse REDIS_URL to extract host and port
parsed_redis_url = urlparse(REDIS_URL)
REDIS_HOST = parsed_redis_url.hostname
REDIS_PORT = parsed_redis_url.port

class Config:
    # Load credentials from the .env file
    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    REDIS_URL = REDIS_URL  # Use the standalone variable
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL