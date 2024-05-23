import random
import sqlite3
import datetime
from telebot import types
from copy import copy


# user_id
# chat_id
# language
# language_change
# date_join

def get_table(message : types.Message, TABLE : str = 'Users') -> dict:
    defaults: dict = {}
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"""SELECT * FROM {TABLE} WHERE chat_id='{message.chat.id}'""")
    defaults['user_id'] = message.from_user.id
    if TABLE == 'Users':
        a = copy(cursor.fetchone())
        defaults['chat_id'] = a[0]
        defaults['language'] = a[1]
        defaults['language_changes'] = a[2]
        defaults['date_join'] = a[3]
        defaults['game_status'] = a[4]
    return defaults


def check_user(chat_id: str) -> bool:
    """
    Checks if the user exists in the database
    :return: if the user exists in the database returns False, else returns True
    """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT chat_id FROM Users WHERE chat_id = {str(chat_id)}
""")
    conn.commit()
    if cursor.fetchone() is None:
        return False
    else:
        return True


def create_user(message: types.Message) -> None:
    """
    Creates new user in the database
    :message
    :return: None
    """
    if not check_user(str(message.chat.id)):
        day, month, year, hour, minutes, seconds = map(int,
                                                       datetime.datetime.now().strftime("%d %m %Y %H %M %S").split(" "))
        date = datetime.datetime(year, month, day, hour, minutes, seconds)
        date = date.timestamp()

        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f""" INSERT INTO 'Users' (chat_id, language, language_changes, date_join, game_status) VALUES( {str(message.chat.id)}, 'None', '0', {int(date)}, 'None' ) ;
            """)
        conn.commit()
        cursor.close()

    def create_coin(user_id: int) -> None:
        conn = sqlite3.connect('base.db')
        cursor = conn.cursor()
        cursor.execute(
            f""" INSERT INTO Users(user_id, language, language_changes, date_join, game_status) VALUES( {str(user_id)}, 'None', '0', {int(date)}, 'None' ) ;
            """)
        conn.commit()
        cursor.close()


def change_information(chat_id: int, name_info: str, new_info_data: str) -> None:
    """
    Change information in database
    :param user_id: user id, that will be used to change user data
    :param name_info: name of information COLUMN
    :param new_info_data: new information for this information COLUMN
    :return: None
    """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""UPDATE Users
        SET {name_info}='{str(new_info_data)}'
        WHERE chat_id={chat_id}"""
    )
    conn.commit()
    cursor.close()


def get_information(chat_id : int, name_info: str, table_name: str = 'Users') -> str:
    """
    Get information out of database
    :param user_id: user id, that will be used to get user data
    :param name_info: name of information COLUMN
    :param table_name: name of table default value 'Users'
    :return: str(cursor.fetchone())
    """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT {name_info} FROM {table_name}
        WHERE user_id = '{chat_id}'
        """
    )
    # cursor.execute(f"""UPDATE Users SET game='True' WHERE user_id={user_id}""")
    conn.commit()
    return clean_fetchone(cursor.fetchone())


def clean_fetchone(fetchone: str) -> str:
    clean_str = ''
    for i in fetchone:
        if fetchone != ("(" or "," or ")"):
            clean_str += i
    return clean_str


def revers_date(date: str | datetime.datetime, no_change_type: bool = False) -> datetime.datetime | float:
    """
    Rechange datetime.timestamp to datetime and back
    :param date: parameter what will be rechange to datatime or datatime.timestamp
    :param no_change_type: parameter what will stop rechange
    :return: parameter of datetime.datetime class
    """
    q = True
    for i in (str(date)):
        if i == ":":
            q = False
            B, b = date.split(' ')
            Y, M, D = map(int, B.split('-'))
            h, m, s = map(int, b.split(':'))
            date1 = datetime.datetime(Y, M, D, h, m, s)
            break
    if q and not no_change_type:
        return datetime.datetime.fromtimestamp(float(date))
    elif not q and not no_change_type:
        return date1.timestamp()
    elif q and no_change_type:
        return datetime.datetime.fromtimestamp(float(date)).timestamp()
    elif not q and no_change_type:
        return datetime.datetime.fromtimestamp(date1.timestamp())



def get_bot_name(language: str) -> str:
    if language == 'US':
        bots_name = ['Karl', 'Mark', 'Jim', 'Alex', 'Robert', 'Bob']
    elif language == 'RU':
        bots_name = ['Александр', 'Дмитрий', 'Стас', 'Юрий', 'Алексей', 'Владислав']
    return random.choice(bots_name)


if __name__ == "__main__":
    pass
