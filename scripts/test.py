#   1715879712.0


import datetime

now = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")

day,month,year,hour,minutes,seconds = map( int, datetime.datetime.now().strftime("%d %m %Y %H %M %S").split(" "))
date = datetime.datetime(year,month,day,hour,minutes,seconds) # create date like 1.1.1970 0:00:00
print(date)
date_timestamp = date.timestamp() # create date like 1715879712.0


def revers_date(date : int | float | datetime.datetime) -> datetime.datetime | float:
    q = 0
    for i in (str(date)):
        if i == ":":
            q = 1
    if q == 0 :
        return datetime.datetime.fromtimestamp(date)
    elif q == 1:
        return date.timestamp()


print(revers_date(date))
print('------------------------------------------')
print(revers_date(date_timestamp))
print('------------------------------------------')
print('------------------------------------------')
print('------------------------------------------')


a = 1715879712.0

a = datetime.datetime.fromtimestamp(a)
print(a)