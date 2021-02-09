import startreactreach
import random
import time

opts = [1, 2, 3, 4]

startreactreach.init()
startreactreach.target(-1)

while 1:
    btn_state=0
    time.sleep(1)
    startreactreach.dostartreact(random.randint(0, 2))
    time_a = time.time()
    while btn_state:
        btn_val = startreactreach.button()
        btn_state = btn_val != b'\x1f'
    startreactreach.target(-1)
    time_b = time.time()
    response_time = time_b-time_a
    print(response_time)
