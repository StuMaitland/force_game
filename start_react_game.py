import startreactreach
import random
import time

opts = [1, 2, 3, 4]

startreactreach.init()

while 1:
    time.sleep(1)
    startreactreach.dostartreact(random.randint(0, 2))
