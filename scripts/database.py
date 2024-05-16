import random
import sqlite3
import datetime

# user_id
# chat_id
# language
# start_use
bots_name = ['Karl', 'Mark', 'Jim', 'Alex', 'Robert', 'Bob']


def check_user(user_id: str | int) -> bool:
    """
    Checks if the user exists in the database
    :param user_id: message.chat.id
    :return: if the user exists in the database returns False, else returns True
    """
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"""
    SELECT user_id FROM Users WHERE user_id = {user_id}
""")
    conn.commit()
    if cursor.fetchone() is None:
        return False
    else:
        return True


def create_user(user_id: int) -> None:
    """
    Creates a new user in the database
    :param user_id: message.chat.id
    :return: None
    """
    day, month, year, hour, minutes, seconds = map(int,
                                                   datetime.datetime.now().strftime("%d %m %Y %H %M %S").split(" "))
    date = datetime.datetime(year, month, day, hour, minutes, seconds)
    date = date.timestamp()

    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""INSERT INTO Users (user_id, language, language_changes, date_join, game_status) VALUES ( {str(user_id)}, {'None'}, {'0'}, {int(date)}, {'None'} );""")
    conn.commit()
    cursor.close()


def change_information(user_id: int, name_info: str, new_info_data: str) -> None:
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""UPDATE Users
        SET {name_info}='{str(new_info_data)}'
        WHERE user_id={user_id}"""
    )
    conn.commit()
    cursor.close()


def get_information(user_id: int, name_info: str, table_name: str = 'Users') -> str:
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(
        f"""SELECT {name_info} FROM {table_name}
        WHERE user_id = '{user_id}'
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

    :param no_change_type:
    :param date:
    :return:
    """
    global date1
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


def exp_language() -> str:
    return "ru"


def get_bot_name() -> str:
    return random.choice(bots_name)


if __name__ == "__main__":
    a = get_information(1442148625, 'user_id')
    print(a)
