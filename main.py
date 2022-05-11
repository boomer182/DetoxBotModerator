import telebot  # import library to work with api telegram
import datetime  # date and time library
import config  # bot config

from db import BotDB
BotDB = BotDB('users_info.db')

users_id_list = []  # list of chat user id`s
days_from_start_list = []  # list of days on which users entered the chat
hours_from_start_list = []

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def is_bot_working(message):
    bot.send_message(message.chat.id, 'Проверка бота! Бот запущен!')

@bot.message_handler(content_types=['new_chat_members'])  # message handler, reacts when a user joins a chat
def kick_user(message):
    if message.author_signature != 'admin':  # admins are not listed
        if (len(days_from_start_list) <= len(users_id_list) or len(users_id_list) == 0):  # day is recorded only 1 time
            users_id_list.append(message.from_user.id)
            days_from_start_list.append(datetime.datetime.today().minute)
            hours_from_start_list.append(datetime.datetime.today().hour)

            BotDB.add_user(message.from_user.id)
            BotDB.add_day(datetime.datetime.today().day)
            BotDB.add_hour(datetime.datetime.today().hour)

            bot.send_message(458950235, f"Отчет: количество участников - {len(users_id_list)}")

    if message.author_signature != 'admin':
        for i in range(0, len(users_id_list)):  # loop in which identical id's are removed
            for j in range(i + 1, len(users_id_list)):
                if users_id_list[i] == users_id_list[j]:
                    del users_id_list[j]
        while 1:  # a cycle in which the bot kicks the user if the difference between the first and current day is 7
            for i in range(0, len(users_id_list)):
                if (datetime.datetime.today().minute - days_from_start_list[i] == 1):
                    bot.ban_chat_member(message.chat.id, users_id_list[i])
                    del users_id_list[i]

bot.polling(none_stop=True)  # the bot is running continuously