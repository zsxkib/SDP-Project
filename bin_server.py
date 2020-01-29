from web_client import WebClient
from camera import Camera
import time
import lycon

client = WebClient('http://localhost:5000')
camera_top = Camera('1.1.3') # when installing make sure the usb port ids match
camera_side = Camera('1.2')

print('entering main loop')
while True:
    print('input signal?')
    input()
    time1 = time.time()
    image_top = camera_top.capture()
    image_side = camera_side.capture()
    time2 = time.time()
    pred_label = client.classify(image_top=image_top, image_side=image_side)
    time3 = time.time()
    print('capture time, prediction time', time2-time1, time3-time2)
    print('prediction label:', pred_label)
    if pred_label == 'unknown':
        print('need manual label for unknown item:')
        mann_label = input()
        print( client.update(mann_label) )
