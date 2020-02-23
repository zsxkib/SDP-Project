import json
import grovepi
import grove_rgb_lcd as lcd
from time import time, sleep
import select
import sys
import move

with open('ports.json', 'r') as f:
    ports = json.load(f)
with open('bins.json', 'r') as f:
    bins= json.load(f)

def when_lid_closed():
    port1 = ports["sensors"]["digital"]["magnetic1"] ##############
    port2 = ports["sensors"]["digital"]["magnetic2"] ##############
    grovepi.pinMode(port1, "INPUT")
    grovepi.pinMode(port2, "INPUT")
    #until both the magnetic switches are released
    while (not grovepi.digitalRead(port1) and not grovepi.digitalRead(port2)):
        sleep(0.1)
    # until atleast one of the magnetic switches are activated
    while (grovepi.digitalRead(port1) or grovepi.digitalRead(port2)):
        sleep(0.1)
    return True

# def output_screen (text, color = "white"): ###########didnt mention port number
#     pallete = {"white":(255,255,255), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "black":(0,0,0)}
#     port = ports["sensors"]["I2C"]["lcd"]
#     lcd.setRGB(pallete[color])
#     lcd.setText(text)

def input_with_timeout(timeout):
    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    if ready:
        return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
    return False

def move_to_bin(category):
    port = ports["sensors"]["digital"]["ultrasonic_horizontal"]
    dist = grovepi.ultrasonicRead(port)
    bin = bins[category]
    if (dist<bin["start_loc"]):
        move.move_front()
    if (dist>bin["end_loc"]):
        move.move_back()
    while (dist>bin["end_loc"] or dist<bin["start_loc"]):
        sleep(0.1)
        dist = grovepi.ultrasonicRead(port)
    move.stop_motors()

def is_bin_full():
    port = ports["sensors"]["digital"]["ultrasonic_vertical"]
    dist = grovepi.ultrasonicRead(port)
    if (dist>50): #bin is empty
        return 0
    elif (dist>25):
        return 0.5
    else:
        return 1

def operate_hatch():
    move.hatch()

def ring_buzzer():
    port = ports["sensors"]["digital"]["buzzer"]
    grovepi.pinMode(port, "OUTPUT")
    grovepi.digitalWrite(port,1)
    sleep(0.5)
    grovepi.digitalWrite(port, 0)
