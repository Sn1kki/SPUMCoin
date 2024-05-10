import random
import sqlite3
import datetime
# user_id
# chat_id
# language
# start_use
bots_name = ['Karl','Mark','Jim','Alex','Robert','Bob']

def check_user(user_id : str | int ) -> bool:
    """
    Checks if the user exists in the database
    :param user_id: message.char.id
    :return: if the user exists in the database returns False, else returns True
    """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT user_id FROM Users WHERE user_id = {user_id}
""")
    conn.commit()
    if cursor.fetchone() == None:
        return False
    else:
        return True


def create_user(user_id : int ) -> None:
    """
    Creates a new user in the database
    :param user_id: message.char.id
    :return: None
    """
    now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    INSERT INTO Users (user_id, language, date_join, game)
    VALUES ({user_id}, {'us'}, {now}, {'None'} )
""")
    conn.commit()
    cursor.close()


def exp_language() -> str:
    return "ru"

def get_bot_name() -> str :
    return random.choice(bots_name)


if __name__ == "__main__":
    create_user(1442148625)