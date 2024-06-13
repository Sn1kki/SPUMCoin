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
    if database.check_table(message.chat.id):
        User = database.get_table(message.chat.id)
        bot.send_message(User['chat_id'], "Error: '<11D0>'")
        bot.send_message(User['chat_id'], "You already exist. Try /menu")
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
    User = database.get_table(callback.message.chat.id)
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
        btn_back = types.InlineKeyboardButton("⏮ Back", callback_data='menu_help')
        markup.add(btn_back)
        bot.edit_message_text(text, User['chat_id'], callback.message.id, reply_markup=markup)
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

    # Menu callback data
    elif callback.data == "menu_profile":
        profile_message(callback.message,True)
    elif callback.data == 'menu_help':
        help_message(callback.message, True)
    elif callback.data == 'menu_about_us':
        about_us(callback.message)
    elif callback.data == 'menu_game':
        pass
    # Profile callback data
    elif callback.data == 'profile_coin_profile':
        pass
    elif callback.data == 'profile_other_profile':
        pass
    elif callback.data == 'profile_edit_profile':
        pass
    elif callback.data == 'profile_delete_profile':
        pass
    elif callback.data == 'profile_back':
        menu_message(callback.message,True)
    # Help callback data
    elif callback.data == 'help_language_change':
        language_change(callback.message)
    elif callback.data == 'help_commands_list':
        commands_list(callback.message, True)
    elif callback.data == 'help_contact_to_support':
        contact_to_support(callback.message)
    elif callback.data == 'help_back':
        menu_message(callback.message, True)


@bot.message_handler(commands=['help'])
def help_message(message, edit=False):
    User = database.get_table(message.chat.id)

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
        text_btn3 = '🛎 Связаться с поддержкой'
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




@bot.message_handler(commands=['menu'])
def menu_message(message, edit=False):
    User = database.get_table(message.chat.id)
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
    btn1 = types.InlineKeyboardButton(text=text_btn1, callback_data='menu_profile')
    btn2 = types.InlineKeyboardButton(text=text_btn2, callback_data='menu_help')
    btn3 = types.InlineKeyboardButton(text=text_btn3, callback_data='menu_about_us')
    btn4 = types.InlineKeyboardButton(text=text_btn4, callback_data='menu_game')
    markup.add(btn1, btn2, btn3, btn4)

    # profile
    # help
    # about (authors + version + git)
    # game
    if not edit:
        bot.send_message(User['chat_id'], text, reply_markup=markup)
    else:
        bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)


def language_change(message):
    User = database.get_table(message.chat.id)
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


def commands_list(message, edit=False):
    User = database.get_table(message.chat.id)

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
    btn_back = types.InlineKeyboardButton(text_btn_back, callback_data='menu_help')
    markup.add(btn_back)

    if not edit:
        bot.send_message(User['chat_id'], text)
    else:
        bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)


def contact_to_support(message):
    User = database.get_table(message.chat.id)
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
    btn_back = types.InlineKeyboardButton(text_btn_back, callback_data='menu_help')
    markup.add(btn_back)

    bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)


@bot.message_handler(commands=['about_us'])
def about_us(message):
    User = database.get_table(message.chat.id)
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
    btn_back = types.InlineKeyboardButton(text_btn_back, callback_data='help_back')
    markup.add(btn1, btn_back)
    bot.edit_message_text(text, User['chat_id'], message.id, reply_markup=markup)


@bot.message_handler(commands=['profile'])
def profile_message(message, edit=False):
    User = database.get_table(message.chat.id)
    date , time = map(str, str(database.revers_date(User['date_join'])).split(' '))
    text_ru = (
        f"Имя пользователя: {User['user_name']}\n"
        f"ID пользователя: {User['user_id']}\n"
        f"\n"
        f"Дата присоединения: {date}\n"
    )
    text_us = (
        f"Username: {User['user_name']}\n"
        f"User ID: {User['user_id']}\n"
        f"\n"
        f"Join date: {date}\n"
    )
    if User['language'] == 'RU':
        text = text_ru
        text_btn1 = "Статистика Coin"
        text_btn2 = "Чужой профиль"
        text_btn3 = "Изменить профиль"
        text_btn4 = "Удалить аккаунт"
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text_btn1 = "Coin Statistics"
        text_btn2 = "Someone else's profile"
        text_btn3 = "Edit profile"
        text_btn4 = "Delete account"
        text_btn_back = '⏮ Back'


    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton(text_btn1, callback_data="profile_coin_profile")
    btn2 = types.InlineKeyboardButton(text_btn2, callback_data="profile_other_profile")
    btn3 = types.InlineKeyboardButton(text_btn3, callback_data="profile_edit_profile")
    btn4 = types.InlineKeyboardButton(text_btn4, callback_data="profile_delete_profile")
    markup.add(btn1,btn2,btn3,btn4)
    if not edit:
        bot.send_message(User['chat_id'],text,reply_markup=markup)
    else:
        markup.add(types.InlineKeyboardButton(text_btn_back,callback_data="profile_back"))
        bot.edit_message_text(text,User['chat_id'],message.id,reply_markup=markup)
    # # Посмотреть статистику coin.
    # Просмотреть чужой профиль.
    # Изменить профиль.
    # Удалить аккаунт
    # # Назад
    #


def profile_other_st(message):
    User = database.get_table(message.chat.id)
    text_ru = (
        f'Вы выбрали пункт "Просмотреть профиль другого пользователя"\n\n'
        f'Напишите ID этого пользователя или нажмите кнопку отмены'
    )
    text_us = (
        f"""You selected "View another user's profile"\n\n"""
        f'Write this user ID or click cancel"'
    )




def profile_other_sd(message):
    is_user = database.check_table(message.text)
    if is_user is True:
        pass

def profile_other_message(message):
    User = database.get_table(message.chat.id)
    Profile = database.get_table(message.text)
    date, time = map(str, str(database.revers_date(Profile['date_join'])).split(' '))
    text_ru = (
        f"Имя пользователя: {Profile['user_name']}\n"
        f"ID пользователя: {Profile['user_id']}\n"
        f"\n"
        f"Дата присоединения: {date}\n"
    )
    text_us = (
        f"Username: {Profile['user_name']}\n"
        f"User ID: {Profile['user_id']}\n"
        f"\n"
        f"Join date: {date}\n"
    )
    if User['language'] == 'RU':
        text = text_ru
        text_btn1 = "Статистика Coin"
        text_btn_back = '⏮ Назад'
    elif User['language'] == 'US':
        text_btn1 = "Coin Statistics"
        text_btn_back = '⏮ Back'
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton(text_btn1, callback_data="profile_other_coin_profile")
    markup.add(btn1)
    markup.add(types.InlineKeyboardButton(text_btn_back, callback_data="menu_profile"))
    bot.edit_message_text(text, message.chat.id, message.id, reply_markup=markup)


bot.polling(none_stop=True, interval=0)
