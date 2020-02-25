import json
from motors import Motors
from time import time, sleep
############### GLOBAL VARIABLES ############
with open('ports.json', 'r') as f:
    ports = json.load(f)
m = ports['motors']['wheels']
h = ports['motors']['hatch']
mc = Motors()
###############################################

def move_front():
    mc.move_motor(m, -100)

def move_back():
    mc.move_motor(m, 100)

def stop_motors():
    mc.stop_motors()

def hatch():
    mc.move_motor(h, -100)
    sleep(1.2)
    mc.stop_motors()
    sleep(1)
    mc.move_motor(h, 100)
    sleep(1.2)
    mc.stop_motors()
