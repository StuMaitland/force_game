import startreactreach
import random
import time

buttons = [1, 2, 3, 4]

startreactreach.init()

while 1:
    for button in random.shuffle(buttons):
        startreactreach.target(0)
        time.sleep(1)

        startreactreach.target(button)
        time.sleep(2)
