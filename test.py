import time 
def happy_birthday():
    t = time.localtime()

    month = t[1]
    day   = t[2]

    if month == 4 and day == 22:
        print("Happy birthday, Ecenur!")
happy_birthday()
