import json
from motors import Motors
from time import time, sleep
############### GLOBAL VARIABLES ############
with open('ports.json', 'r') as f:
    ports = json.load(f)
f1 = ports["motors"]["f1"]
f2 = ports["motors"]["f2"]
r1 = ports["motors"]["r1"]
r2 = ports["motors"]["r2"]
h1 = ports["motors"]["h1"]
h2 = ports["motors"]["h2"]
mc = Motors()
###############################################

def move_front():
    mc.move_motor(f1, 100)
    mc.move_motor(f2, 100)
    mc.move_motor(r1, -100)
    mc.move_motor(r2, -100)

def move_back():
    mc.move_motor(r1, 100)
    mc.move_motor(r2, 100)
    mc.move_motor(f1, -100)
    mc.move_motor(f2, -100)

def stop_motors():
    mc.stop_motors()

def hatch():
    mc.move_motor(h1, 80)
    mc.move_motor(h2, 80)
    sleep(1.2)
    mc.stop_motors()
    mc.move_motor(h1, -80)
    mc.move_motor(h2, -80)
    sleep(1.2)
    mc.stop_motors()