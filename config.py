from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = getenv('API_TOKEN')
APP_URL = getenv('APP_URL')
DB_URL = getenv('DB_URL')
DB_NAME = getenv('DB_NAME')
DB_USERNAME = getenv('DB_USERNAM')
DB_PASSWORD = getenv('DB_PASSWORD')
DB_HOST = getenv('DB_HOST')
DB_PORT = getenv('DB_PORT')
CHAT_ID = getenv('CHAT_ID')