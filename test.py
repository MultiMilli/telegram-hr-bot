# from datetime import datetime
from os import getenv
from logging import DEBUG

from telebot import TeleBot, types, logger
from flask import Flask, request

from models import User
# from config import API_TOKEN, APP_URL

TOKEN = '5719924088:AAHqL_qZq-ePYkEjRlKzaSmf9YB46gTrQ-0'
bot = TeleBot(TOKEN)
URL = f'https://tl-test-tg.herokuapp.com/5719924088:AAHqL_qZq-ePYkEjRlKzaSmf9YB46gTrQ-0'
server = Flask(__name__)
# logger = logger
# logger.setLevel(DEBUG)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not User.select().where(User.chat_id == message.chat.id):
        User.create(chat_id=message.chat.id, username=message.from_user.username, first_name=message.from_user.first_name)
        bot.send_message(message.chat.id, f'Hello i\'am working - USER will be create')
    else:
        bot.send_message(message.chat.id, f'User already created')

@server.route('/5719924088:AAHqL_qZq-ePYkEjRlKzaSmf9YB46gTrQ-0', methods=['POST'])
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