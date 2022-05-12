import telebot  # import library to work with api telegram
import datetime  # date and time library
from config import *  # bot config
import psycopg2  # postgresql

from db import BotDB
BotDB = BotDB(DB_URI)  # connect with bd to the project

bot = telebot.TeleBot(TOKEN)

chat_id = -1001780597173  # id of chat detox

users_id_list = []

@bot.message_handler(commands=['start'])  # bot is on or off
def is_bot_working(message):
    bot.send_message(message.chat.id, 'Проверка бота! Бот запущен!')

@bot.message_handler(content_types=['new_chat_members'])  # message handler, reacts when a user joins a chat
def get_data(message):
    id = message.from_user.id
    if message.author_signature != 'admin':  # admins are not listed
        users_id_list.append(id)

        BotDB.cursor.execute(f"SELECT user_id FROM users WHERE user_id = {id}")
        result = BotDB.cursor.fetchone()

        if not result:
            BotDB.add_data(id, datetime.datetime.today().day)

@bot.message_handler(content_types=['text', 'photo', 'video'])
def kick_user(message):
    BotDB.cursor.execute("SELECT join_data_day FROM users")
    result_day = BotDB.cursor.fetchall()

    BotDB.cursor.execute("SELECT user_id FROM users")
    result_id = BotDB.cursor.fetchall()

    for i in range(0, len(result_day)):
        j = 0
        if (datetime.datetime.today().day - result_day[i][j] >= 7):
            bot.ban_chat_member(message.chat.id, result_id[i])

    bot.send_message(458950235, f"Отчет: количество участников - {bot.get_chat_member_count(message.chat.id)}")

    if bot.get_chat_member_count(message.chat.id) < 4:
        BotDB.delete_data()
        bot.send_message(message.chat.id, 'Пользователи успешно удалены!')

bot.polling(none_stop=True)  # the bot is running continuously