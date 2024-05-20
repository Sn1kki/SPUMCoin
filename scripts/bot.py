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
    database.create_user(message.chat.id)
    User = database.get_table(message)
    text = (
        "Welcome to SPUMCoin!\n"
        "Choose your language\n"
    )
    btn = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='English', callback_data='sus')
    btn2 = types.InlineKeyboardButton(text='Russian', callback_data='sru')
    btn.add(btn1, btn2)

    database.create_user(User['chat_id'])

    bot.send_message(User['chat_id'], text, reply_markup=btn)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback(callback):
    User = database.get_table(callback.message)
    if callback.data == 'sus':
        text = (
            "Welcome to SPUMCoin!\n"
            "This bot is under development\n"
            "We apologize for the inconvenience caused\n"
            "Try /help command"
        )

        database.change_information(User['chat_id'], 'language', 'US')

        bot.edit_message_text(text, User['chat_id'], callback.message.id)
    elif callback.data == 'sru':
        text = (
            "Добро пожаловать в SPUMCoin.\n"
            "Данный бот находится в разработке\n"
            "Приносим свои извинения за предоставленные неудобства\n"
            "Попробуйте команду /help"
        )

        database.change_information(User['chat_id'], 'language', 'RU')

        bot.edit_message_text(text, User['chat_id'], callback.message.id)
    elif callback.data == 'eus':
        text = (
            "Changes complete\n"
            "Now your interface language is english\n"
            "Code: '<Lcus>'"
        )

        database.change_information(User['chat_id'], 'language', 'US')
        changes_count = User['language_changes']
        database.change_information(User['chat_id'], 'language_changes', str(changes_count))

        bot.edit_message_text(text, User['chat_id'], callback.message.id)
    elif callback.data == 'eru':
        text = (
            "Изменения применены\n"
            "Теперь язык вашего интерфейса русский\n"
            "Code: '<Lcru>'"
        )

        database.change_information(User['chat_id'], 'language', 'RU')
        changes_count = User['language_changes']
        database.change_information(User['chat_id'], 'language_changes', str(changes_count))

        bot.edit_message_text(text, User['chat_id'], callback.message.id)


@bot.message_handler(commands=['help'])
def help_message(message):
    User = database.get_table(message)

    text_ru = (
        f"Приветствую!\n"
        f"Вы обратились к техническую поддержку бота Spum Coin.\n"
        f"С вами работает: Бот {database.get_bot_name(User['language'])} \n\n"
        f"Что вас интересует в данную минуту?"

    )

    text_us = (
        f"Welcome!\n"
        f"You have contacted the technical support of the Spum Coin bot.\n"
        f"Working with you: Bot {database.get_bot_name(User['language'])} \n\n"
        f"What interests you at this moment?"
    )

    if User['language'] == 'RU':
        text = text_ru
    elif User['language'] == 'US':
        text = text_us

    markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    btn1 = types.KeyboardButton('✳ Изменить язык')
    btn2 = types.KeyboardButton('🛠 Команды')
    btn3 = types.KeyboardButton('🛎 Связаться с поддержкой')
    markup.add(btn1, btn2, btn3)

    bot.send_message(User['chat_id'], text, reply_markup=markup)





@bot.message_handler(commands=['game_text'])
def run_cmd(message):
    User = database.get_table(message)
    text = """ 12434255"""
    bot.send_message(message.chat.id,text)

@bot.message_handler(content_types=['text'])
def text_message(message):
    User = database.get_table(message)
    if message.text == "✳ Изменить язык":
        language_change(message)
    elif message.text == "🛠 Команды":
        commands_list(message)
    elif message.text == '🛎 Связаться с поддержкой':
        technical_support(message)

def language_change(message):
    User = database.get_table(message)
    text_us = (
        f"Your language: English\n"
        "Choose your language\n"
    )
    text_ru = (
        f"Ваш язык: Русский'\n"
        "Выберите язык\n"
    )
    if User['language'] == 'RU':
        text = text_ru
    elif User['language'] == 'US':
        text = text_us

    btn = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text='English', callback_data='eus')
    btn2 = types.InlineKeyboardButton(text='Russian', callback_data='eru')
    btn.add(btn1, btn2)

    bot.send_message(User['chat_id'], text, reply_markup=btn)


def commands_list(message):
    User = database.get_table(message)

    text = (
        "/start -- Начинает программу\n"
        "/help -- Вызывает меню помощи\n"
        "/run -- Запускает игру"
    )

    bot.send_message(User['chat_id'], text)


def technical_support(message):
    chat_id = message.chat.id
    text = (
        "Техническая поддержка сейчас не доступна\n"
        "Code: '<Error 000>'"
    )
    bot.send_message(chat_id, text)


@bot.message_handler(commands=['send db'])
def send_db(message):
    pass


bot.polling(none_stop=True, interval=0)
