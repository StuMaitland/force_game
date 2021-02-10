import startreactreach
import random
import time
import csv
from datetime import datetime

startreactreach.init()
startreactreach.target(-1)

response_times = []
trial_types = []
i = 0

while i < 10:
    i += 1
    btn_state = 1
    time.sleep(1)
    trial = random.choices([0, 1, 2], [0.33, 0.33, 0.33])[0]
    startreactreach.dostartreact(trial)
    time_a = time.time()
    while btn_state:
        btn_val = startreactreach.button()
        btn_state = btn_val == b'\x1f'
    startreactreach.target(-1)
    time_b = time.time()
    response_times.append(time_b - time_a)
    trial_types.append(trial)

with open('start_react_{}.txt'.format(datetime.now()), mode='w') as f:
    writer = csv.writer(f)
    for k, v in enumerate(response_times):
        writer.writerow([trial_types[k], response_times[k]])

