import telebot
from telebot import types
import database

with open("token.txt", 'r') as token_file:
    token: str = token_file.read()

bot = telebot.TeleBot(token)


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
            "None"
        )
        bot.send_message(chat_id, text)
    elif callback.data == 'btn2':
        text = (
            "Рад вас видеть в моём  боте.\n"
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


    bot.send_message(chat_id, text)

@bot.message_handler(content_types=['text'])
def send_welcome(message):
    bot.delete_message(message.chat.id, message.id)


bot.polling(non_stop=True)
