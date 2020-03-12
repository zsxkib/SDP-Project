from electroMagnet import *
from gpio import *
from camera import Camera
from sense import *
from web_client import WebClient # ML server
from grovepi import *
import grove_rgb_lcd as lcd
import wave

import select
import sys
import move_over_web as move

from matplotlib import pyplot as plt
from threading import Thread
import time

import sys
sys.path.insert(1, './interface') # path to the interface
#from interfaceWebApp import WebInterface

print("123123")

avg_window = []
usread_window_size = 5
usread_port = 3
def usread():
    print('usread avg', avg_window)
    if len(avg_window) > 0:
        avg_window.pop(0)
    while len(avg_window) < usread_window_size:
        avg_window.append( grovepi.ultrasonicRead(usread_port) )
    return sum(avg_window) / usread_window_size

n_collects = 0
collect_mode = False # change this to collect sample

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
        self.MLServer = WebClient('http://192.168.192.200:5000')
        
        # initialise the electro magnet locks
        stopMagnet() # release the locks

        # initialise the i2c lcd screen
        self.ledRed = pinMode(ports['sensors']['digital']['ledRed'],"OUTPUT")
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
        #print('islidopen', counter, res)
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
        dist = usread() #grovepi.ultrasonicRead(port)
        bin = bins[category]
        print("dist",dist, bin)
        if (dist<bin["start_pos"]):
            move.move_front()
        if (dist>bin["end_pos"]):
            move.move_back()
        while (dist>bin["end_pos"] or dist<bin["start_pos"]):
            sleep(0.1)
            dist = usread() #grovepi.ultrasonicRead(port)
            print("dist",dist)
        move.stop_motors()


        if self.is_bin_full():
            if category == 'non-recyclable':
                # ask user to clear up the bin, stop here
                self.output_screen('The bins are full!!!')
                digitalWrite(self.ledRed,1) 
            else:
                self.move_to_bin('non-recyclable')
        else:
            self.operate_hatch()
            digitalWrite(self.ledRed,1) 
            


    def is_bin_full(self):
        return False
        port = ports["sensors"]["digital"]["ultrasonic_vertical"]
        dist = grovepi.ultrasonicRead(port)
        print(dist)
        if (dist>50): #bin is empty
            print('bin empty')
            return 0
        elif (dist>25):
            print('bin half')
            return 0.5
        else:
            print('bin full')
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
        global n_collects
        global collect_mode

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
                sound_clip = self.camera_side.record_binary()

                if collect_mode:
                    n_collects += 1
                    with wave.open(f'collects/{n_collects}.wav', 'wb') as wavefile:
                        wavefile.setnchannels(1)
                        wavefile.setsampwidth(2) # s16_le
                        wavefile.setframerate(48000)
                        wavefile.writeframes(sound_clip)
                    plt.imsave(f'collects/{n_collects}.png', image_top)
                    print('collected sample', n_collects)
                #plt.imsave('top.png', image_top)
                #plt.imsave('side.png', image_side)

                # TODO: fix here
                if collect_mode:
                    pred_label = 'trash'
                else:
                    pred_label = self.MLServer.classify(image_top=image_top, image_side=image_side)

                print(f'the predicted label is {pred_label}')
                if pred_label == 'metal':
                    pred_label = 'metal'
                elif pred_label != 'trash':
                    pred_label = 'recyclable'
                else:
                    pred_label = 'non-recyclable'

                if pred_label == 'metal':
                    lcd_content = 'Metal recyclable'
                elif pred_label == 'cardboard':
                    lcd_content = 'Cardboard recyclable'
                elif pred_label == 'recyclable':
                    lcd_content = 'Other recyclable'
                elif pred_label == 'non-recyclable':
                    lcd_content = 'Non-recyclable'
                else:
                    lcd_content = 'Error, dump into trash'
                    pred_label = 'non-recyclable'

                self.output_screen(lcd_content)
                if not collect_mode:
                    self.move_to_bin(pred_label)



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
