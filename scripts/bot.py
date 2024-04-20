import telebot
from telebot import types
import database

with open("token.txt", 'r') as token_file:
    token: str = token_file.read()

bot = telebot.TeleBot(token)

basic_markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=1 ,one_time_keyboard=True)
bnt_bm = types.KeyboardButton("hide me")
basic_markup.add(bnt_bm)

hide_markup = types.ReplyKeyboardRemove()

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    text_us = (
        "Welcome to SPUMCoin!\n"
        "Choose your language\n"
    )

    text = text_us

    btn = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='English', callback_data='btn1')
    btn2 = types.InlineKeyboardButton(text='Russian', callback_data='btn2')
    btn.add(btn1, btn2)

    bot.send_message(chat_id, text, reply_markup=btn)


@bot.callback_query_handler(func= lambda callback: callback.data)
def callback(callback):
    chat_id = callback.message.chat.id
    if callback.data == 'btn1':
        text = (
            "Welcome to SPUMCoin!\n"
            "Try /help command"
        )
        bot.send_message(chat_id, text)
    elif callback.data == 'btn2':
        text = (
            "Добро пожаловать в SPUMCoin.\n"
            "Попробуйте команду /help"
        )
        bot.send_message(chat_id, text)


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


    bot.send_message(chat_id, text,reply_markup=markup)

@bot.message_handler(content_types=['text'])
def text_message(message):

    chat_id = message.chat.id
    if message.text == "✳ Изменить язык": pass


def language_change(message):
    chat_id = message.chat.id
    text_us = (
        "\n"
        "Choose your language\n"
    )

    text = text_us

    btn = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='English', callback_data='btn1')
    btn2 = types.InlineKeyboardButton(text='Russian', callback_data='btn2')
    btn.add(btn1, btn2)

    bot.send_message(chat_id, text, reply_markup=btn)

bot.polling(non_stop=True)
