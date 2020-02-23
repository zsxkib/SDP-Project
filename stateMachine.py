from electroMagnet import *
from gpio import *
from camera import Camera
from web_client import WebClient
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
        self.currentState = startingState

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
        self.lcd = None


    @property
    def state(self):
        return self.currentState

    def isLidOpen(self):
        if gpio_read(self.triggerPin) == 1: return True
        else: return False

    def run(self):
        # the main loop:
        while True:
            print(f'State update: {self.state}')
            if self.state == 'idle':
                stopMagnet()
                # turn off the lights
                while not self.isLidOpen():
                    pass 
                # if self.isLidOpen():
                self.state = 'lidUp'
                
            elif self.state == 'lidUp':
                while self.isLidOpen():
                    pass
                self.state = 'lidDown'

            elif self.state == 'lidDown':
                # lit up the lights

                # lock the lid
                runMagnet()

                self.state = 'processing'
                
            elif self.state == 'processing':
                # image_top = camera_top.capture()
                image_top = image_side = self.camera_side.capture()
                plt.imsave('top.png', image_top)
                plt.imsave('side.png', image_side)

                time.sleep(5)
                # TODO: fix here
                pred_label = self.client.classify(image_top=image_top, image_side=image_side)
                
                if pred_label == 'metal':
                    pass
                elif pred_label == 'cardboard':
                    pass
                elif pred_label == 'recyclable':
                    pass
                elif pred_label == 'non-recyclable':
                    pass
                else:
                    pass

                # finished trash sorting
                self.state = 'idle'

            # elif self.state == 'moving':
            #     pass
            # elif self.state == 'returning':
            #     pass
            elif self.state == 'shutDown':
                break
        
        

if __name__ == '__main__':
    robot = Recycltron()
    # print(robot.state)
    robot.run()
