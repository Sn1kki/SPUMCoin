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
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
user_id INTEGER,
chat_id INTEGER,
language TEXT
)
''')
    conn.commit()
    conn.close()


bots_name = ['Karl','Mark','Jim','Alex','Robert','Bob']

def start_data_input(User_id, Chat_id, Language):
    con = sqlite3.connect('base.db')

    cur = con.cursor()
    cur.execute("select user_id from Users where user_id=?", (User_id,))
    data = cur.fetchall()
    if data is None:
        print('not found')
    else:
        print('found')

def exp_language() -> str:
    return "ru"

def get_bot_name() -> str :
    return random.choice(bots_name)