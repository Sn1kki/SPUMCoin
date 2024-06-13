from telebot import TeleBot, types

with open("token.txt", 'r') as token_file:
    token: str = token_file.read()

bot = TeleBot(token)


@bot.message_handler(commands=['start'])
def send_welcome(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text='Привет, как твое имя?')
    bot.register_next_step_handler(message, get_name)


def get_name(message: types.Message):
    print(message.text)
    # тут у вас то что ввел юзер
    bot.send_message(chat_id=message.chat.id, text=f'Приятно познакомиться, {message.text}\n'
                                                   f'А сколько тебе лет?')
    bot.register_next_step_handler(message, get_age)


def get_age(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=f'Вау тебе уже, {message.text} лет\n'
                                                   f'Как настроение?')
    bot.register_next_step_handler(message, get_mood)


def get_mood(message: types.Message):
    bot.send_message(chat_id=message.chat.id, text=f'Отлично!\n')


@bot.message_handler(commands=['pups'])
def pups(message):
    q = 0
    text = ''
    for i in str(message.text):
        if q != 0:
            text += i
        if i == ' ':
            q += 1
    if q == 1 and str.isdigit(text):
        text = str.isdigit(text)
    else:
        text = ''
    bot.send_message(message.chat.id, text )



bot.infinity_polling(skip_pending=True)
