import telebot
from telebot import types
import database

with open("token.txt", 'r') as token_file:
    token: str = token_file.read()

bot = telebot.TeleBot(token)
"""
basic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1 ,one_time_keyboard=True)
bnt_bm = types.KeyboardButton("hide me")
basic_markup.add(bnt_bm)

hide_markup = types.ReplyKeyboardRemove()
"""

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    text = (
        "Welcome to SPUMCoin!\n"
        "Choose your language\n"
    )
    print(message.chat.id)
    btn = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='English', callback_data='sus')
    btn2 = types.InlineKeyboardButton(text='Russian', callback_data='sru')
    btn.add(btn1, btn2)

    bot.send_message(chat_id, text, reply_markup=btn)


@bot.callback_query_handler(func= lambda callback: callback.data)
def callback(callback):
    chat_id = callback.message.chat.id
    if callback.data == 'sus':
        text = (
            "Welcome to SPUMCoin!\n"
            "This bot is under development\n"
            "We apologize for the inconvenience caused\n"
            "Try /help command"
        )
        bot.edit_message_text(text, chat_id, callback.message.id)
    elif callback.data == 'sru':
        text = (
            "Добро пожаловать в SPUMCoin.\n"
            "Данный бот находится в разработке\n"
            "Приносим свои извинения за предоставленные неудобства\n"
            "Попробуйте команду /help"
        )
        bot.edit_message_text(text, chat_id, callback.message.id)
    elif callback.data == 'eus':
        text = (
            "Changes complete\n"
            "Now your interface language is english\n"
            "Code: '<Lcus>'"
        )
        bot.edit_message_text(text, chat_id, callback.message.id)
    elif callback.data == 'eru':
        text = (
            "Изменения применены\n"
            "Теперь язык вашего интерфейса русский\n"
            "Code: '<Lcru>'"
        )
        bot.edit_message_text(text, chat_id, callback.message.id)


@bot.message_handler(commands=['help'])
def help_message(message):
    chat_id = message.chat.id

    text_ru = (
        f"Приветствую!\n"
        f"Вы обратились к техническую поддержку бота Spum Coin.\n"
        f"С вами работает: Bot {database.get_bot_name()} \n\n"
        f"Что вас интересует в данную минуту?"

    )

    text_us = 'None'

    if database.exp_language() == "ru": text = text_ru
    else: text = text_us

    markup = types.ReplyKeyboardMarkup(row_width=1,resize_keyboard=True,one_time_keyboard=True)
    btn1 = types.KeyboardButton('✳ Изменить язык')
    btn2 = types.KeyboardButton('🛠 Команды')
    btn3 = types.KeyboardButton('🛎 Связаться с поддержкой')
    markup.add(btn1, btn2, btn3)


    bot.send_message(chat_id, text, reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_message(message):

    chat_id = message.chat.id
    if message.text == "✳ Изменить язык": language_change(message)
    elif message.text == "🛠 Команды": commands_list(message)
    elif message.text == '🛎 Связаться с поддержкой': technical_support(message)

@bot.message_handler(commands=['run'])
def run_cmd(message):
    chat_id = message.chat.id
    text = """ 
"""

def language_change(message):
    chat_id = message.chat.id
    text_us = (
        f"Your language: '<None>'\n"
        "Choose your language\n"
    )

    text = text_us

    btn = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='English', callback_data='eus')
    btn2 = types.InlineKeyboardButton(text='Russian', callback_data='eru')
    btn.add(btn1, btn2)

    bot.send_message(chat_id, text, reply_markup=btn)

def commands_list(message):
    chat_id = message.chat.id
    text = (
        "/start -- Начинает программу\n"
        "/help -- Вызывает меню помощи\n"
        "/run -- Запускает игру"
    )
    bot.send_message(chat_id,text)

def technical_support(message):
    chat_id = message.chat.id
    text = (
        "Техническая поддержка сейчас не доступна\n"
        "Code: '<Error 000>'"
    )
    bot.send_message(chat_id,text)

@bot.message_handler(commands=['send db'])
def send_db(message):
    pass
bot.polling(non_stop=True,interval=0)
