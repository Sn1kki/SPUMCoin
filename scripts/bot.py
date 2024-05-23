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

[[[]]]



"""





@bot.message_handler(commands=['start'])
def send_welcome(message):
    if database.check_user(message.chat.id):
        User = database.get_table(message)
        bot.send_message(User['chat_id'],"Error: '<11D0>'")
        bot.send_message(User['chat_id'],"You already exist. Try /menu")
    else:
        database.create_user(message)
        User = database.get_table(message)
        text = (
            "Welcome to SPUMCoin!\n"
            "Choose your language\n"
        )
        btn = types.InlineKeyboardMarkup(row_width=1)
        btn1 = types.InlineKeyboardButton(text='English', callback_data='start_us')
        btn2 = types.InlineKeyboardButton(text='Russian', callback_data='start_ru')
        btn.add(btn1, btn2)

        bot.send_message(User['chat_id'], text, reply_markup=btn)


@bot.callback_query_handler(func=lambda callback: callback.data)
def callback(callback):
    User = database.get_table(callback.message)
    if callback.data == 'start_us':
        text = (
            "Welcome to SPUMCoin!\n"
            "\n"
            "This bot is under development\n"
            "We apologize for the inconvenience caused\n"
            "\n"
            "Try /menu command"
        )

        database.change_information(User['chat_id'], 'language', 'US')

        bot.edit_message_text(text, User['chat_id'], callback.message.id)
    elif callback.data == 'start_ru':
        text = (
            "Добро пожаловать в SPUMCoin.\n"
            "\n"
            "Данный бот находится в разработке\n"
            "Приносим свои извинения за предоставленные неудобства\n"
            "\n"
            "Попробуйте команду /menu"
        )

        database.change_information(User['chat_id'], 'language', 'RU')

        bot.edit_message_text(text, User['chat_id'], callback.message.id)
    elif callback.data == 'language_edit_us':
        text = (
            "Changes complete\n"
            "Now your interface language is english\n"
            "Code: '<Lcus>'"
        )

        database.change_information(User['chat_id'], 'language', 'US')
        changes_count = User['language_changes']
        database.change_information(User['chat_id'], 'language_changes', str(changes_count))

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_back = types.InlineKeyboardButton("⏮ Back",callback_data='menu_help')
        markup.add(btn_back)
        bot.edit_message_text(text, User['chat_id'], callback.message.id,reply_markup=markup)
    elif callback.data == 'language_edit_ru':
        text = (
            "Изменения применены\n"
            "Теперь язык вашего интерфейса русский\n"
            "Code: '<Lcru>'"
        )

        database.change_information(User['chat_id'], 'language', 'RU')
        changes_count = User['language_changes']
        database.change_information(User['chat_id'], 'language_changes', str(changes_count))

        markup = types.InlineKeyboardMarkup(row_width=1)
        btn_back = types.InlineKeyboardButton("⏮ Назад", callback_data='menu_help')
        markup.add(btn_back)

        bot.edit_message_text(text, User['chat_id'], callback.message.id, reply_markup=markup)
    elif callback.data == 'help_back':
        menu_message(callback.message, True)
    elif callback.data == 'menu_help':
        help_message(callback.message,True)
    elif callback.data == 'menu_about_us':
        about_us(callback.message)
    elif callback.data == 'help_language_change':
        language_change(callback.message)
    elif callback.data == 'help_commands_list':
        commands_list(callback.message,True)
    elif callback.data == 'help_contact_to_support':
        contact_to_support(callback.message)


@bot.message_handler(commands=['help'])
def help_message(message, edit=False):
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

    if User['language'] == 'RU':
        text_btn1 = '✳ Изменить язык'
        text_btn2 = '🛠 Команды'
        text_btn3 =  '🛎 Связаться с поддержкой'
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text_btn1 = '✳ Change language'
        text_btn2 = '🛠 Commands'
        text_btn3 = '🛎 Contact to support'
        text_btn_back = '⏮ Back'


    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text_btn1, callback_data='help_language_change')
    btn2 = types.InlineKeyboardButton(text_btn2, callback_data='help_commands_list')
    btn3 = types.InlineKeyboardButton(text_btn3, callback_data='help_contact_to_support')
    markup.add(btn1, btn2, btn3)

    if not edit:
        bot.send_message(User['chat_id'], text, reply_markup=markup)
    else:
        btn_back = types.InlineKeyboardButton(text_btn_back, callback_data='help_back')
        markup.add(btn_back)
        bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)





@bot.message_handler(commands=['game_text'])
def run_cmd(message):
    User = database.get_table(message)
    text = """ 12434255"""
    bot.send_message(message.chat.id,text)


@bot.message_handler(commands=['menu'])
def menu_message(message, edit=False):
    User = database.get_table(message)
    text_ru = (
        f"Добро пожаловать в меню SPUM Coin\n"
        f"Спасибо, что стали пользоваться нашем ботом\n"
        f"\n"
        f"Выберете интересующий вас пункт\n"
        f"По всем вопросам обращайтесь в /help\n"
        f"\n"
        f"Приятного время препровождения\n"
    )
    text_us = (
        f"Welcome to the SPUM Coin menu\n"
        f"Thank you for using our bot\n"
        f"\n"
        f"Select the item you are interested in\n"
        f"For all questions, contact /help\n"
        f"\n"
        f"Have a nice time\n"
    )
    if User['language'] == 'RU':
        text = text_ru
        text_btn1 = "Профиль"
        text_btn2 = "Помощь"
        text_btn3 = "О нас"
        text_btn4 = "Игра"
    elif User['language'] == 'US':
        text = text_us
        text_btn1 = "Profile"
        text_btn2 = "Help"
        text_btn3 = "About us"
        text_btn4 = "Game"

    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text=text_btn1,callback_data='menu_profile')
    btn2 = types.InlineKeyboardButton(text=text_btn2,callback_data='menu_help')
    btn3 = types.InlineKeyboardButton(text=text_btn3,callback_data='menu_about_us')
    btn4 = types.InlineKeyboardButton(text=text_btn4,callback_data='menu_game')
    markup.add(btn1,btn2,btn3,btn4)



    # profile
    # help
    # about (authors + version + git)
    # game
    if not edit:
        bot.send_message(User['chat_id'],text,reply_markup=markup)
    else:
        bot.edit_message_text(text,User['chat_id'],message.id, reply_markup=markup)



def language_change(message):
    User = database.get_table(message)
    text_us = (
        f"Your language: English\n"
        "Choose your language\n"
    )
    text_ru = (
        f"Ваш язык: Русский\n"
        "Выберите язык\n"
    )
    if User['language'] == 'RU':
        text = text_ru
        text_btn1 = 'Английский'
        text_btn2 = 'Русский'
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text = text_us
        text_btn1 = 'English'
        text_btn2 = 'Russian'
        text_btn_back = '⏮ Back'

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text_btn1, callback_data='language_edit_us')
    btn2 = types.InlineKeyboardButton(text_btn2, callback_data='language_edit_ru')
    btn_back = types.InlineKeyboardButton(text_btn_back, callback_data='menu_help')
    markup.add(btn1, btn2, btn_back)

    bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)


def commands_list(message,edit = False):
    User = database.get_table(message)

    text_ru = (
        f"/start -- Начинает программу\n"
        f"/menu -- Вызывает меню общего доступа\n"
        f"/profile -- Показывает информацию о профиле\n"
        f"/help -- Вызывает меню помощи\n"
    )

    text_us = (
        f"/start -- Starts the program\n"
        f"/menu -- Calls up the sharing menu\n"
        f"/profile -- Shows profile information\n"
        f"/help -- Calls up the help menu\n"
    )

    if User['language'] == 'RU':
        text = text_ru
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text = text_us
        text_btn_back = '⏮ Back'

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_back = types.InlineKeyboardButton(text_btn_back,callback_data='menu_help')
    markup.add(btn_back)

    if not edit:
        bot.send_message(User['chat_id'], text)
    else:
        bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)

def contact_to_support(message):
    User = database.get_table(message)
    text_ru = (
        "Техническая поддержка сейчас не доступна\n"
        "Code: '<Error 000>'"
    )
    text_us = (
        "Technical support is currently unavailable\n"
        "Code: '<Error 000>'"
    )

    if User['language'] == 'RU':
        text = text_ru
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text = text_us
        text_btn_back = '⏮ Back'

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn_back = types.InlineKeyboardButton(text_btn_back,callback_data='menu_help')
    markup.add(btn_back)

    bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)


@bot.message_handler(commands=['about_us'])
def about_us(message):
    User = database.get_table(message)
    text_ru = (
        f"Приветствую вас!\n"
        f"\n"
        f"Данный проект реализовывает один человек,\n"
        f"@Sn1kki -> Я :)))\n"
        f"\n"
        f"Так же отдельная благодарность пользователю\n"
        f"@FedorTyulpin\n"
        f"И всем, тем, кто участвовал в создании проекта.\n"
        f"\n"
        f"\n"
        f"Весь код данного бота открытый и находится на GitHub\n"
    )
    text_us = (
        f"Hello!\n"
        f"\n"
        f"This project is being implemented by one person\n"
        f"@Sn1kki -> Me :)))\n"
        f"\n"
        f"Also special thanks to the user\n"
        f"@FedorTulpin\n"
        f"And everyone who participated in the creation of the project.\n"
        f"\n"
        f"\n"
        f"All code for this bot is open source and located on GitHub\n"
    )

    if User['language'] == 'RU':
        text = text_ru
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text = text_us
        text_btn_back = '⏮ Back'

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton('📄 GitHub', url='https://github.com/Sn1kki/SPUMCoin')
    btn_back = types.InlineKeyboardButton(text_btn_back,callback_data='help_back')
    markup.add(btn1,btn_back)
    bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)




@bot.message_handler(commands=['send db'])
def send_db(message):
    pass


bot.polling(none_stop=True, interval=0)
