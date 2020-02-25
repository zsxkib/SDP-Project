from electroMagnet import *
from gpio import *
from camera import Camera
from sense import *
from web_client import WebClient
import grove_rgb_lcd as lcd

import select
import sys
import move

from matplotlib import pyplot as plt
from threading import Thread
import move
import time

class Recycltron:
    States = {
        'idle': "idle",
        'lidUp': "lidUp",
        'lidDown': "lidDown",
        'processing': "processing",
        # 'moving': "moving",
        # 'returning': "returning",
        # 'shutDown': "shutDown"
    }
    
    def __init__(self, startingState = 'idle', triggerPin = 25):
        self.state = startingState

        with open('ports.json', 'r') as f:
            self.ports = json.load(f)
        with open('bins.json', 'r') as f:
            self.bins= json.load(f)

        # set up the magnetic trigger
        self.triggerPin = triggerPin
        gpio_setup(self.triggerPin)

        # set up the cameras
        # self.camera_top = Camera('1.1.3') # when installing make sure the usb port ids match
        self.camera_side = Camera('1.2')

        # connecting to the classifier server
        self.client = WebClient('http://192.168.192.200:5000')
        
        # initialise the electro magnet locks
        stopMagnet() # release the locks

        # initialise the i2c lcd screen
        self.led = pinMode(ports['digital']['led'],"OUTPUT")
        self.lastText = None


    def isLidOpen(self, N=100):
	# drift towards -inf if open else towards +inf
        counter = 0
        while abs(counter) < N:
            res = gpio_read(self.triggerPin)
            if res == 1:
                counter += 1
            else:
                counter -= 1
        print('islidopen', counter, res)
        if counter < 0: return True
        else: return False

    def output_screen(self, text, color = "green"): ###########didnt mention port number
        pallete = {"white":(255,255,255), "red":(255,0,0), "green":(0,255,0), "blue":(0,0,255), "black":(0,0,0)}
        # port = ports["sensors"]["I2C"]["lcd"]
        if text != self.lastText:
            # lcd.setRGB(pallete[color][0], pallete[color][1], pallete[color][2])
            lcd.setText_norefresh(text)
            self.lastText = text

    def input_with_timeout(self, timeout):
        ready, _, _ = select.select([sys.stdin], [], [], timeout)
        if ready:
            return sys.stdin.readline().rstrip('\n')  # expect stdin to be line-buffered
        return False

    def move_to_bin(self, category):
        port = ports["sensors"]["digital"]["ultrasonic_horizontal"]
        dist = grovepi.ultrasonicRead(port)
        bin = bins[category]
        print("dist",dist)
        if (dist<bin["start_pos"]):
            move.move_front()
        if (dist>bin["end_pos"]):
            move.move_back()
        while (dist>bin["end_pos"] or dist<bin["start_pos"]):
            sleep(0.1)
            dist = grovepi.ultrasonicRead(port)
            print("dist",dist)
        move.stop_motors()


    def is_bin_full(self):
        port = ports["sensors"]["digital"]["ultrasonic_vertical"]
        dist = grovepi.ultrasonicRead(port)
        print(dist)
        if (dist>50): #bin is empty
            return 0
        elif (dist>25):
            return 0.5
        else:
            return 1

    def operate_hatch(self):
        move.hatch()

    def ring_buzzer(self):
        port = ports["sensors"]["digital"]["buzzer"]
        grovepi.pinMode(port, "OUTPUT")
        grovepi.digitalWrite(port,1)
        sleep(0.5)
        grovepi.digitalWrite(port, 0)


    def run(self):
        # the main loop:
        while True:
            print(f'State update: {self.state}')
            if self.state == 'idle':
                self.output_screen('Machine: idle.')
                stopMagnet()
                # turn off the lights
                while not self.isLidOpen():
                    pass
                # if self.isLidOpen():
                self.state = 'lidUp'

            elif self.state == 'lidUp':
                self.output_screen('Lid is open')
                while self.isLidOpen():
                    pass
                self.state = 'lidDown'

            elif self.state == 'lidDown':
                self.output_screen('Lid closed      and locked')
                # lit up the lights

                # lock the lid
                runMagnet()
                time.sleep(3)
                self.state = 'processing'

            elif self.state == 'processing':
                self.output_screen('Processing      item')
                # image_top = camera_top.capture()
                image_top = image_side = self.camera_side.capture()
                plt.imsave('top.png', image_top)
                plt.imsave('side.png', image_side)

                # TODO: fix here
                pred_label = self.client.classify(image_top=image_top, image_side=image_side)
                print(f'the predicted label is {pred_label}')
                if pred_label == 'metal':
                    self.output_screen('Metal recyclable')
#                    move_to_bin(pred_label)
                elif pred_label == 'cardboard':
                    self.output_screen('Cardboard recyclable')
#                    move_to_bin(pred_label)
                elif pred_label == 'recyclable':
                    self.output_screen('Other recyclable')
#                    move_to_bin(pred_label)
                elif pred_label == 'non-recyclable':
                    self.output_screen('Non-recyclable')
#                    move_to_bin(pred_label)
                else:
                    self.output_screen('Error, dump into trash')
#                    move_to_bin('non-recyclable')

                # finished trash sorting
                self.state = 'idle'

            # elif self.state == 'moving':
            #     pass
            # elif self.state == 'returning':
            #     pass
            elif self.state == 'shutDown':
                self.output_screen('Error, dump into trash')
                break
        
        

if __name__ == '__main__':
    robot = Recycltron()
    # print(robot.state)
    robot.run()
