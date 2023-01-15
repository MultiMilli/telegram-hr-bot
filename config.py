from os import getenv

from dotenv import load_dotenv

load_dotenv()

API_TOKEN = getenv('API_TOKEN')
USERNAME = getenv('USERNAME')
PASSWORD = getenv('PASSWORD')
APP_URL = getenv('APP_URL')