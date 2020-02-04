from motors import Motors
from time import time, sleep

#################### varirables need to be declared ###########
f1 = 2
f2 = 3
r1 = 4
r2 = 5
h1 = 1
h2 = 0
###############################################################

#f1,f2- front motors 1&2
#r1,r2- rear motors 1&2
#time in second
def move_front(timer): #front and rear motor_id
    mc = Motors()

    #motor_id=1
    #speed=100 #speed is from 0 to 100
    run_time=timer

    #mc.move_motor(motor_id, speed)
    mc.move_motor(f1,-100)
    mc.move_motor(f2,-100)
    mc.move_motor(r1,100)
    mc.move_motor(r2,100)

    start_time = time()
    while time() < start_time+run_time:
        sleep(0.1) #has 50ms accuracy
    mc.stop_motors()

#f1,f2- front motors 1&2
#r1,r2- rear motors 1&2
#time in second
def move_back(timer): #front and rear motor_id
    mc = Motors()

    #motor_id=1
    #speed=100 #speed is from 0 to 100
    run_time=timer

    #mc.move_motor(motor_id, speed)
    mc.move_motor(f1,100)
    mc.move_motor(f2,100)
    mc.move_motor(r1,-100)
    mc.move_motor(r2,-100)

    start_time = time()
    while time() < start_time+run_time:
        sleep(0.1) #has 50ms accuracy
    mc.stop_motors()

def stop_motors():
    mc = Motors()
    mc.stop_motors()

def hatch():
    #open hatch
    mc = Motors()
    run_time = 1
    mc.move_motor(h1,-80)
    start_time = time()
    while time() < start_time+run_time:
        sleep(0.1) #has 50ms accuracy
    mc.stop_motors()
    sleep(1)
    #close hatch
    run_time = 1
    mc.move_motor(h1,80)
    start_time = time()
    while time() < start_time+run_time:
        sleep(0.1) #has 50ms accuracy
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
