# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

class Config:
    SECRET_KEY = os.getenv('JWT_SECRET')
    MONGO_URI = os.getenv('DB_CONNECTION_STRING')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')
    HASH_PASSWORD_ALGORITHM = os.getenv('HASH_PASSWORD_ALGORITHM')
    SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')  # Default to 127.0.0.1 if not set
    SERVER_PORT = int(os.getenv('SERVER_PORT', 5000))  # Default to 5000 if not set
