import telebot  # import library to work with api telegram
import datetime  # date and time library
from config import * # bot config

from db import BotDB
BotDB = BotDB(DB_URI)  # connect with bd to the project

# db_connection = psycopg2.connect(DB_URI, sslmode="require")
# db_object = db_connection.cursor()

users_id_list = []  # list of chat user id`s
days_from_start_list = []  # list of days on which users entered the chat

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])  # bot is on or off
def is_bot_working(message):
    bot.send_message(message.chat.id, 'Проверка бота! Бот запущен!')

@bot.message_handler(content_types=['new_chat_members'])  # message handler, reacts when a user joins a chat
def kick_user(message):
    if message.author_signature != 'admin':  # admins are not listed
        if (len(days_from_start_list) <= len(users_id_list) or len(users_id_list) == 0):  # day is recorded only 1 time
            users_id_list.append(message.from_user.id)
            days_from_start_list.append(datetime.datetime.today().day)

            BotDB.add_data(message.from_user.id, datetime.datetime.today().day) # add user id and join day to bd

            bot.send_message(458950235, f"Отчет: количество участников - {len(users_id_list)}")

    if message.author_signature != 'admin':
        for i in range(0, len(users_id_list)):  # loop in which identical id's are removed
            for j in range(i + 1, len(users_id_list)):
                if users_id_list[i] == users_id_list[j]:
                    del users_id_list[j]
        while 1:  # a cycle in which the bot kicks the user if the difference between the first and current day is 7
            for i in range(0, len(users_id_list)):
                if (datetime.datetime.today().day - days_from_start_list[i] == 7):
                    bot.ban_chat_member(message.chat.id, users_id_list[i])
                    del users_id_list[i]
                    if (len(users_id_list) == 0): bot.send_message(message.chat.id, 'Пользователи успешно удалены!')

bot.polling(none_stop=True)  # the bot is running continuously