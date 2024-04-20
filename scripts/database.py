import random
# user_id
# chat_id
# language
# start_use


bots_name = ['Karl','Mark','Jim','Alex','Robert','Bob']

def exp_language() -> str:
    return "ru"

def get_bot_name() -> str :
    return random.choice(bots_name)