from motors import Motors
from time import time, sleep

#################### varirables need to be declared ###########
f1 = 2
f2 = 3
r1 = 4
r2 = 5
h1 = 1
h2 = 0
###################### global variables #######################
mc = Motors()
###############################################################

#time in second
def move_front(timer):

    #mc.move_motor(motor_id, speed)
    mc.move_motor(f1,-100)
    mc.move_motor(f2,-100)
    mc.move_motor(r1,100)
    mc.move_motor(r2,100)

    sleep(timer)
    mc.stop_motors()

#time in second
def move_back(timer):

    #mc.move_motor(motor_id, speed)
    mc.move_motor(f1,100)
    mc.move_motor(f2,100)
    mc.move_motor(r1,-100)
    mc.move_motor(r2,-100)

    sleep(timer)
    mc.stop_motors()

def stop_motors():
    mc.stop_motors()

def hatch():
    #open hatch
    mc.move_motor(h1,-80)
    sleep(1)
    mc.stop_motors()
    sleep(1)
    #close hatch
    mc.move_motor(h1,80)
    sleep(1)
    mc.stop_motors()


def bin0():
    hatch()
    stop_motors()

def bin1():
    move_front(4)
    stop_motors()
    hatch()
    stop_motors()
    move_back(4)
    stop_motors()
