import startreactreach
import random
import time
from picamera import PiCamera
from datetime import datetime
import csv

buttons = [1, 2, 3, 4]

min_wait = 3
max_wait = 4
i = 0

event_times = []
reaction_times = []
button_indices = []

camera = PiCamera()
camera.resolution = (1280, 720)
camera.start_recording('target_reach_{}.h264'.format(datetime.now()))
start_time = time.time()
while i < 10:
    random.shuffle(buttons)
    i += 1
    for button in buttons:
        startreactreach.target(0)
        time.sleep(random.uniform(min_wait, max_wait))

        startreactreach.target(button)
        time_a = time.time()
        btn_state = 1
        while btn_state:
            btn_val = startreactreach.button()
            btn_state = btn_val == b'\x1f'
        startreactreach.target(-1)
        time_b = time.time()

        event_times.append(time_a-start_time)
        reaction_times.append(time_b-time_a)
        button_indices.append(button)

camera.stop_recording()
with open('target_reach_{}.txt'.format(datetime.now()), mode='w') as f:
    writer = csv.writer(f)
    for k, v in enumerate(event_times):
        writer.writerow([button_indices[k], event_times[k], reaction_times[k]])
