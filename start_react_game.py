import startreactreach
import random
import time

buttons = [1, 2, 3, 4]

#startreactreach.init()

while 1:
    random.shuffle(buttons)
    for button in buttons:
        #startreactreach.target(0)
        print(0)
        time.sleep(1)

        #startreactreach.target(button)
        print(button)
        time.sleep(2)
