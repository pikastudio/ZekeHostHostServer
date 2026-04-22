import data
import time
def ask():
    data.startsplashscreen()
    a = input(data.inputfile)
    if a == "3":
        data.openyt()
        time.sleep(2)
        ask()
    elif a == "2":
        print("Bye")
    elif a == "1":
        data.startserver()
    else:
        print("what")
        ask()
ask()