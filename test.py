# from datetime import datetime
from os import getenv
from logging import DEBUG

from telebot import TeleBot, types, logger
from flask import Flask, request

# from models import User
from config import API_TOKEN, APP_URL

bot = TeleBot(API_TOKEN)
URL = APP_URL + API_TOKEN
server = Flask(__name__)
logger = logger
logger.setLevel(DEBUG)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Hello i\'am working')

@server.route(f'/{API_TOKEN}', methods=['POST'])
def redirect_message():
    json_string = request.get_data().decode('utf-8')
    update = types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return '!', 200

@server.route('/')
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=URL)
    return '!', 200


if __name__ == '__main__':
    server.run(host='0.0.0.0', port=int(getenv('PORT', 5000)))