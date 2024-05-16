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
    :param user_id: message.chat.id
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
    :param user_id: message.chat.id
    :return: None
    """
    day,month,year,hour,minutes,seconds = map( int, datetime.datetime.now().strftime("%d %m %Y %H %M %S").split(" "))
    date = datetime.datetime(year,month,day,hour,minutes,seconds)
    print(date)
    date_timestamp = date.timestamp()
    print(date_timestamp)
    date_undo = datetime.datetime.fromtimestamp(date_timestamp)
    print(date_undo)
    conn = sqlite3.connect('base.db')
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO Users (user_id, language, date_join, game) VALUES ( {str(user_id)} , 'us' , {int(date_timestamp)} , 'None' );""")
    conn.commit()
    cursor.close()

def revers_date(date : str | int | float | datetime.datetime) -> datetime.datetime | float:
    """

    :param date:
    :return:
    """
    q = True
    for i in (str(date)):
        if i == ":":
            q = False
            B , b = date.split(' ')
            Y , M , D = map( int , B.split('-') )
            h , m , s = map( int , b.split(':') )
            date = datetime.datetime(Y,M,D,h,m,s)
            break
    if q :
        return datetime.datetime.fromtimestamp(float(date))
    if not q:
        return date.timestamp()

def exp_language() -> str:
    return "ru"

def get_bot_name() -> str :
    return random.choice(bots_name)


if __name__ == "__main__":
    pass
