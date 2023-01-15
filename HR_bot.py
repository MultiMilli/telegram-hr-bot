from datetime import datetime
from os import getenv
from logging import DEBUG

from telebot import TeleBot, types, logger
from flask import Flask, request

from models import User
from config import API_TOKEN, APP_URL

# import logging
# logger = telebot.logger
# telebot.logger.setLevel(logging.DEBUG)

bot = TeleBot(API_TOKEN) #API_TOKEN get from the enviroment variables
URL = APP_URL + API_TOKEN
server = Flask(__name__)
logger = logger
logger.setLevel(DEBUG)

Q_INDEX = 0
ANSWERS_LIST = []
APPLICATION_DATETIME = 0

with open('questions.txt', 'r') as file:
    questions_list = [i[:-1] for i in file.readlines()]

@bot.message_handler(commands=['start'])
def send_welcome(message):

    global Q_INDEX
    global ANSWERS_LIST
    global APPLICATION_DATETIME

    button = types.InlineKeyboardButton('💸 Вперед 💸', callback_data='go')
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(button)

    if not User.select().where(User.chat_id == message.chat.id):
        User.create(chat_id=message.chat.id, username=message.from_user.username, first_name=message.from_user.first_name)
        bot.send_message(
            message.chat.id, 
            f'Привіт <b>{message.chat.first_name}</b>👋, я помічник ТОПОВОЇ арбітражної команди <b>TrafficLab</b>!🔥 '
            f'Бажаєш змінити своє життя та розвиватися в сфері арбітражу? Тоді ми чекаємо на тебе! '
            f'Пропоную відповісти на декілька питань та ми обов\'язково зв\'яжемось з тобою 🤙', 
            reply_markup=keyboard, 
            parse_mode='HTML')
    else:
        user = User.get(User.chat_id == message.chat.id)
        if user.apply_time and (datetime.now() - user.apply_time).seconds < 30:
            bot.send_message(
                message.chat.id, 
                f'❗️Вибачте, але повторна подача заявок можлива не раніше ніж за <b>1 тиждень</b>❗️', 
                parse_mode='HTML'
            )
        else:
            bot.send_message(
                message.chat.id, 
                f'Якщо вам не вдалось повністю заповнити заявку, або хочете подати її повторно, ' 
                f'скористайтесь кнопкую <b>"Почати"</b>, або надішліть будь-яке повідомлення в чат!', 
                reply_markup=keyboard,
                parse_mode='HTML'
            )
            Q_INDEX = 0
            ANSWERS_LIST = []
            APPLICATION_DATETIME = 0  

@bot.callback_query_handler(func=lambda call: True)
def send_welcome(call):
    
    global Q_INDEX
    
    if call.data == 'go':
        bot.send_message(
            call.message.chat.id, 
            questions_list[Q_INDEX]
        )
        Q_INDEX += 1

@bot.message_handler(content_types=['text'])
def answer_handler(message):
   
    global Q_INDEX
    global APPLICATION_DATETIME

    user = User.get(User.chat_id == message.chat.id)

    if Q_INDEX == 0: 
        bot.send_message(
            message.chat.id, 
            questions_list[Q_INDEX]
        )
        Q_INDEX += 1
    else:
        if APPLICATION_DATETIME == 0:
            ANSWERS_LIST.append(message.text)
            try:
                bot.send_message(
                    message.chat.id,
                    f'{questions_list[Q_INDEX]}'
                )
                Q_INDEX += 1
            except IndexError:
                bot.send_message(
                    message.chat.id, 
                    f'Дякую за відповіді, на все добре!🙌'
                )
                APPLICATION_DATETIME = datetime.now()
                user.apply_time = APPLICATION_DATETIME
                user.save()
                msg = []
                msg.append(f'<b>ID:</b> {user.id}\n')
                msg.append(f'<b>Username:</b> @{user.username}\n')
                msg.append(f'<b>First Name:</b> {user.first_name}\n')
                msg.append(f'<b>Application time:</b> {user.apply_time.strftime("%d.%m.%Y %H:%M:%S")}\n')
                for answer in ANSWERS_LIST:
                    msg.append(f'<b>{ANSWERS_LIST.index(answer) + 1}.</b> {answer}\n')
                bot.send_message(
                    chat_id='-1001800698387', 
                    text=''.join(msg), 
                    parse_mode='HTML'
                )
        elif (datetime.now() - user.apply_time).seconds < 30:
            bot.send_message(
                message.chat.id, 
                f'❗️Вибачте, але повторна подача заявок можлива не раніше ніж за <b>1 тиждень</b>❗️',
                parse_mode='HTML'
            )  
        else:
            bot.send_message(
                message.chat.id, 
                f'Якщо бажаєте заповнити заявку ще раз, застосуйте команду <b>/start</b>, або перезапустіть бота!',
                parse_mode='HTML'
            )

@server.route('/' + API_TOKEN, methods=['POST'])
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
    # bot.infinity_polling()
