import random
import sqlite3
# user_id
# chat_id
# language
# start_use
if __name__ == "__main__":
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Users 
    ''')


bots_name = ['Karl','Mark','Jim','Alex','Robert','Bob']



def exp_language() -> str:
    return "ru"

def get_bot_name() -> str :
    return random.choice(bots_name)