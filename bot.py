import telebot # библиотека telebot
from config import token # импорт токена

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, message)
    bot.reply_to(message, "Привет! Я бот для управления чатом.")

@bot.message_handler(commands=['ban'])
def ban_user(message):
    if message.reply_to_message: #проверка на то, что эта команда была вызвана в ответ на сообщение 
        chat_id = message.chat.id # сохранение id чата
         # сохранение id и статуса пользователя, отправившего сообщение
        user_id = message.reply_to_message.from_user.id
        user_status = bot.get_chat_member(chat_id, user_id).status 
         # проверка пользователя
        # if user_status == 'administrator' or user_status == 'creator':
        if user_status in ('administrator', 'creator'): # Другой варик if
            bot.reply_to(message, "Невозможно забанить администратора.")
        else:
            bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
            bot.reply_to(message, f"Пользователь @{message.reply_to_message.from_user.username} был забанен.")
    else:
        bot.reply_to(message, "Эта команда должна быть использована в ответ на сообщение пользователя, которого вы хотите забанить.")


@bot.message_handler(content_types=['new_chat_members'])
def make_some(message):
    bot.send_message(message.chat.id, f'Новый участник @{message.new_chat_members[0].username} зашёл к нам!')
    bot.approve_chat_join_request(message.chat.id, message.from_user.id)
    

@bot.message_handler(content_types=['left_chat_member'])
def make_something(message):
    bot.send_message(message.chat.id, f'Участник @{message.left_chat_member.username} покинул нас(')
    bot.decline_chat_join_request(message.chat.id, message.from_user.id)

@bot.message_handler(func=lambda message: "https://" in message.text.lower())
def ban_message(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_status = bot.get_chat_member(chat_id, user_id).status 
    if user_status in ('administrator', 'creator'): # Другой варик if
        bot.reply_to(message, "Невозможно забанить администратора.")
    else:
        bot.ban_chat_member(chat_id, user_id) # пользователь с user_id будет забанен в чате с chat_id
        bot.reply_to(message, f"Пользователь был забанен.")

bot.infinity_polling(none_stop=True)
